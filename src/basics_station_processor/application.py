import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Any

import aiohttp
from pydoover.models import ScheduleEvent
from pydoover.processor import Application

from .app_config import BasicStationProcessorConfig
from .app_tags import BasicStationProcessorTags
from .app_ui import BasicStationProcessorUI

log = logging.getLogger(__name__)

STATS_PATH = "/api/v3/gs/gateways/{gateway_id}/connection/stats"
DURATION_RE = re.compile(r"^([0-9]*\.?[0-9]+)\s*([a-zµ]*)$")
DURATION_TO_MS = {
    "ns": 1e-6,
    "us": 1e-3,
    "µs": 1e-3,
    "ms": 1.0,
    "s": 1000.0,
    "m": 60_000.0,
    "h": 3_600_000.0,
    "": 1000.0,  # protobuf default Duration is seconds
}


def _parse_duration_ms(value: Any) -> float | None:
    """Parse a protobuf Duration JSON value (e.g. ``"0.123s"``) into milliseconds."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value) * 1000.0
    match = DURATION_RE.match(str(value).strip())
    if not match:
        return None
    magnitude, unit = match.groups()
    factor = DURATION_TO_MS.get(unit.lower())
    if factor is None:
        return None
    return float(magnitude) * factor


def _parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


class BasicStationProcessor(Application):
    config_cls = BasicStationProcessorConfig
    ui_cls = BasicStationProcessorUI
    tags_cls = BasicStationProcessorTags

    config: BasicStationProcessorConfig
    tags: BasicStationProcessorTags
    ui: BasicStationProcessorUI

    async def on_schedule(self, event: ScheduleEvent):
        region = self.config.tts_region.value
        gateway_id = self.config.gateway_id.value
        api_key = self.config.api_key.value

        if not gateway_id or not api_key:
            log.warning("Gateway ID or API key not configured; skipping fetch.")
            return

        url = f"https://{region}.cloud.thethings.network" + STATS_PATH.format(
            gateway_id=gateway_id
        )
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

        log.info(f"Fetching gateway stats for {gateway_id} from {region}.")
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 404:
                    # TTN returns 404 when the gateway has never connected.
                    log.info("Gateway has never connected — no stats available yet.")
                    await self._mark_disconnected()
                    return
                resp.raise_for_status()
                stats = await resp.json()

        await self._publish(stats)

    async def _mark_disconnected(self):
        await self.tags.connected.set(False)

    async def _publish(self, stats: dict[str, Any]):
        connected_at = _parse_datetime(stats.get("connected_at"))
        disconnected_at = _parse_datetime(stats.get("disconnected_at"))
        is_connected = connected_at is not None and disconnected_at is None

        await self.tags.connected.set(is_connected)
        await self.tags.protocol.set(stats.get("protocol"))
        await self.tags.connected_at.set(stats.get("connected_at"))
        await self.tags.last_status_at.set(stats.get("last_status_received_at"))

        await self.tags.uplink_count.set(_parse_int(stats.get("uplink_count")))
        await self.tags.downlink_count.set(_parse_int(stats.get("downlink_count")))
        await self.tags.tx_ack_count.set(
            _parse_int(stats.get("tx_acknowledgment_count"))
        )
        await self.tags.last_uplink_at.set(stats.get("last_uplink_received_at"))
        await self.tags.last_downlink_at.set(stats.get("last_downlink_received_at"))

        rtt = stats.get("round_trip_times") or {}
        await self.tags.rtt_median_ms.set(_parse_duration_ms(rtt.get("median")))
        await self.tags.rtt_count.set(_parse_int(rtt.get("count")))

        metrics = ((stats.get("last_status") or {}).get("metrics")) or {}
        await self.tags.rx_received.set(_parse_int(metrics.get("rxnb")))
        await self.tags.rx_ok.set(_parse_int(metrics.get("rxok")))
        await self.tags.rx_forwarded.set(_parse_int(metrics.get("rxfw")))
        await self.tags.tx_received.set(_parse_int(metrics.get("txin")))
        await self.tags.tx_ok.set(_parse_int(metrics.get("txok")))

        if is_connected:
            await self.ping_connection(
                online_at=datetime.now(timezone.utc),
                offline_at=datetime.now(timezone.utc) + timedelta(minutes=15),
            )

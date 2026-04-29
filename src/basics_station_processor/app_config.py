from pathlib import Path

from pydoover import config
from pydoover.processor import ScheduleConfig


class BasicStationProcessorConfig(config.Schema):
    dv_proc_schedules = ScheduleConfig(
        default="rate(5 minutes)",
        description="How often to poll TTN for gateway stats.",
    )
    position = config.ApplicationPosition()

    tts_region = config.String(
        "TTN Region",
        default="au1",
        description="TTN cluster region (e.g. au1, eu1, nam1).",
    )
    gateway_id = config.String(
        "Gateway ID",
        description="The TTN gateway ID, as registered in the Console.",
    )
    api_key = config.String(
        "TTN Console API Key",
        description=(
            "API key with 'View gateway information' and 'View gateway status' "
            "rights. Used to query gateway connection stats from TTN."
        ),
    )


def export():
    BasicStationProcessorConfig.export(
        Path(__file__).parents[2] / "doover_config.json",
        "basics_station_processor",
    )

from pathlib import Path

from pydoover import ui

from .app_tags import BasicStationProcessorTags as T


class TrafficSubmodule(ui.Submodule):
    uplink_count = ui.NumericVariable("Uplinks", value=T.uplink_count, precision=0)
    downlink_count = ui.NumericVariable("Downlinks", value=T.downlink_count, precision=0)
    tx_ack_count = ui.NumericVariable("TX Acks", value=T.tx_ack_count, precision=0)
    last_uplink_at = ui.DateTimeVariable("Last Uplink", value=T.last_uplink_at)
    last_downlink_at = ui.DateTimeVariable("Last Downlink", value=T.last_downlink_at)


class RoundTripSubmodule(ui.Submodule):
    rtt_median_ms = ui.NumericVariable(
        "Median",
        value=T.rtt_median_ms,
        units="ms",
        precision=1,
    )
    rtt_count = ui.NumericVariable("Sample Count", value=T.rtt_count, precision=0)


class RadioMetricsSubmodule(ui.Submodule):
    rx_received = ui.NumericVariable("Packets Received", value=T.rx_received, precision=0)
    rx_ok = ui.NumericVariable("CRC OK", value=T.rx_ok, precision=0)
    rx_forwarded = ui.NumericVariable("Forwarded", value=T.rx_forwarded, precision=0)
    tx_received = ui.NumericVariable("TX Received", value=T.tx_received, precision=0)
    tx_ok = ui.NumericVariable("TX OK", value=T.tx_ok, precision=0)


class BasicStationProcessorUI(ui.UI):
    connected = ui.BooleanVariable("Connected", value=T.connected)
    protocol = ui.TextVariable("Protocol", value=T.protocol)
    connected_at = ui.DateTimeVariable("Connected At", value=T.connected_at)
    last_status_at = ui.DateTimeVariable("Last Status", value=T.last_status_at)

    traffic = TrafficSubmodule("Traffic")
    rtt = RoundTripSubmodule("Round Trip Time")
    metrics = RadioMetricsSubmodule("Radio Metrics")


def export():
    BasicStationProcessorUI(None, None, None).export(
        Path(__file__).parents[2] / "doover_config.json",
        "basics_station_processor",
    )

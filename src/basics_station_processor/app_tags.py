from pydoover.tags import Tag, Tags


class BasicStationProcessorTags(Tags):
    connected = Tag("boolean", default=None)
    protocol = Tag("string", default=None)
    connected_at = Tag("string", default=None)
    last_status_at = Tag("string", default=None)

    uplink_count = Tag("integer", default=None)
    downlink_count = Tag("integer", default=None)
    tx_ack_count = Tag("integer", default=None)
    last_uplink_at = Tag("string", default=None)
    last_downlink_at = Tag("string", default=None)

    rtt_median_ms = Tag("number", default=None)
    rtt_count = Tag("integer", default=None)

    rx_received = Tag("integer", default=None)
    rx_ok = Tag("integer", default=None)
    rx_forwarded = Tag("integer", default=None)
    tx_received = Tag("integer", default=None)
    tx_ok = Tag("integer", default=None)

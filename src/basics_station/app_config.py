from pydoover import config


class BasicStationConfig(config.Schema):
    tc_key = config.String(
        "TTN API Key",
        description=(
            "API key from TTN with 'Link as Gateway to a Gateway Server "
            "for traffic exchange' rights. Used for LNS authentication."
        ),
    )
    gateway_eui = config.String(
        "Gateway EUI",
        default="",
        pattern="^([0-9A-Fa-f]{16})?$",
        description=(
            "16-char hex EUI matching the Gateway EUI registered in TTN. "
            "Leave blank to fall back to the MAC-derived default."
        ),
    )
    tts_region = config.String(
        "TTN Region",
        default="au1",
        description="TTN cluster region (e.g. au1, eu1, nam1).",
        advanced=True,
    )
    model = config.String(
        "Concentrator Model",
        default="AUTO",
        description="Concentrator hardware model (RAK2287 = SX1302 USB).",
        advanced=True,
    )
    device_path = config.String(
        "Device Path",
        default="AUTO",
        description=(
            "Concentrator serial device, e.g. a /dev/serial/by-id/... path. "
            "AUTO probes every ttyACM/ttyUSB port, which disrupts other serial "
            "devices (e.g. the Doovit IO board), so set this explicitly."
        ),
        advanced=True,
    )
    interface = config.String(
        "Interface",
        default="AUTO",
        description="Concentrator interface (auto, usb, spi).",
        advanced=True,
    )


def export():
    from pathlib import Path
    BasicStationConfig().export(Path(__file__).parents[2] / "doover_config.json", "basics_station")

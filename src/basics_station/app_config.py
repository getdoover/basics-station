from pathlib import Path

from pydoover import config


class BasicsStationConfig(config.Schema):
    outputs_enabled = config.Boolean("Digital Outputs Enabled", default=True)
    funny_message = config.String("A Funny Message")  # required — no default given
    sim_app_key = config.Application("Simulator App Key", description="The app key for the simulator")


def export():
    BasicsStationConfig.export(Path(__file__).parents[2] / "doover_config.json", "basics_station")

if __name__ == "__main__":
    export()

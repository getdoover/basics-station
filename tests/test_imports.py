"""Smoke tests for the template application.

These validate that modules are importable, the config schema is well-formed,
the Tags/UI classes subclass the correct bases, and the config export entry
point runs end-to-end.
"""

import json

from pydoover.config import Schema
from pydoover.tags import Tags
from pydoover.ui import UI


def test_import_app():
    from basics_station.application import BasicsStationApplication
    assert BasicsStationApplication.config_cls is not None
    assert BasicsStationApplication.tags_cls is not None
    assert BasicsStationApplication.ui_cls is not None


def test_config_schema():
    from basics_station.app_config import BasicsStationConfig
    assert issubclass(BasicsStationConfig, Schema)

    schema = BasicsStationConfig.to_schema()
    assert isinstance(schema, dict)
    assert schema["type"] == "object"
    assert len(schema["properties"]) > 0
    assert "a_funny_message" in schema["required"]
    assert "simulator_app_key" in schema["required"]


def test_tags():
    from basics_station.app_tags import SampleTags
    assert issubclass(SampleTags, Tags)


def test_ui():
    from basics_station.app_ui import BasicsStationUI
    assert issubclass(BasicsStationUI, UI)


def test_state_machine():
    from basics_station.app_state import BasicsStationState
    state = BasicsStationState()
    assert state.state == "off"


def test_config_export(tmp_path):
    from basics_station.app_config import BasicsStationConfig

    fp = tmp_path / "doover_config.json"
    BasicsStationConfig.export(fp, "basics_station")

    data = json.loads(fp.read_text())
    assert "basics_station" in data
    assert "config_schema" in data["basics_station"]
    assert "properties" in data["basics_station"]["config_schema"]


def test_ui_export(tmp_path):
    from basics_station.app_ui import BasicsStationUI

    fp = tmp_path / "doover_config.json"
    BasicsStationUI(None, None, None).export(fp, "basics_station")

    data = json.loads(fp.read_text())
    assert "ui_schema" in data["basics_station"]
    assert data["basics_station"]["ui_schema"]["type"] == "uiApplication"
    assert "is_working" in data["basics_station"]["ui_schema"]["children"]

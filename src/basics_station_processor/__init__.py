from typing import Any

from pydoover.processor import run_app

from .application import BasicStationProcessor


def handler(event: dict[str, Any], context):
    run_app(BasicStationProcessor(), event, context)

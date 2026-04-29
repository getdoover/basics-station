from pydoover.docker import run_app

from .application import BasicsStationApplication

def main():
    """Run the application."""
    run_app(BasicsStationApplication())

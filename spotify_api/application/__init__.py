from fastapi import FastAPI

from spotify_api.infrastructure import CheckCharts, CheckTracks


def create_app():
    app = FastAPI()
    CheckCharts.check()
    CheckTracks.check()

    return app

import sys
import os

src_path = os.path.abspath("src")
sys.path.append(src_path)

from kedro.config import ConfigLoader
from kedro.framework.project import settings
from fastapi import FastAPI
from src.api import prediction_weather, train_model_frocast, train_model_predict
import uvicorn

conf_path = str(settings.CONF_SOURCE)
conf_loader = ConfigLoader(conf_source=conf_path, env="local")

host = conf_loader["credentials"]["uvicorn"]["UVICORN_HOST"]
port = conf_loader["credentials"]["uvicorn"]["UVICORN_PORT"]
reload = conf_loader["credentials"]["uvicorn"]["UVICORN_RELOAD"]

FROZEN_APP = FastAPI(
    title="Frozen",
    version="0.0.1",
    )


FROZEN_APP.include_router(train_model_frocast.router)
FROZEN_APP.include_router(prediction_weather.router)
FROZEN_APP.include_router(train_model_predict.router)


if __name__ == "__main__":
    uvicorn.run("run_api:FROZEN_APP",
                host = host,
                port = port,
                reload = reload)
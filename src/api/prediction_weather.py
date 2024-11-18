import pathlib
from typing import Any, Iterable
from kedro.runner import SequentialRunner
from fastapi import APIRouter
from kedro.framework.context import KedroContext
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)

# PROJ_DIR = pathlib.Path(__file__).parent

def get_session(dict_string : dict) -> Iterable[KedroSession]:
    bootstrap_project(pathlib.Path().cwd())
    with KedroSession.create(extra_params = dict_string) as session:
        return session

def get_context(session) -> Iterable[KedroContext]:
    return session.load_context()

class WeatherRequest(BaseModel):
    start_date: str
    Latitude: str
    Longitude: str
    Altitude: str
    class Config:
        schema_extra = {
            "example": {
                "start_date":"2023-09-10 00:00:00+00:00",
                "Latitude":"48.756",
                "Longitude":"4.5897",
                "Altitude":"100"
            }
        }

router  = APIRouter()

@router.post("/weather/frozen/probabilty")
async def prob_frozein(input_row : WeatherRequest): 
    try: 
        input_data = json.loads(input_row.json())
        session  = get_session({"ROW_STRING" : input_data})
        context  = get_context(session)
        catalog = context.catalog
        session.run(pipeline_name  = "proba_frozen", runner=SequentialRunner(is_async=True))
        return catalog.load("proba_frozen")
    except Exception as e:
        # Log the error with the appropriate level and stack trace
        logger.error("An error occurred in prediction_weather():", exc_info=True)
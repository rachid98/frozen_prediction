from fastapi import APIRouter
from api.prediction_weather import get_context, get_session
from pydantic import BaseModel
from kedro.runner import SequentialRunner
import json
import logging

logger = logging.getLogger(__name__)


router  = APIRouter()

@router.post("/weather/frozen/training_forcasting_models")
async def train_forecast_models(input_row = None): 
    try: 
        input_data = json.loads(input_row.json())
        session  = get_session({"ROW_STRING" : input_data})
        context  = get_context(session)
        catalog = context.catalog
        session.run(pipeline_name  = "train_model_frocast", runner=SequentialRunner(is_async=True))
        return catalog.load("dict_forecasting_model")
    except Exception as e:
        # Log the error with the appropriate level and stack trace
        logger.error("An error occurred in list__train_model_TS():", exc_info=True)
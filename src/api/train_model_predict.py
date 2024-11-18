from fastapi import APIRouter
from api.prediction_weather import get_context, get_session
from pydantic import BaseModel
from kedro.runner import SequentialRunner
import json
import logging

logger = logging.getLogger(__name__)


router  = APIRouter()

@router.post("/weather/frozen/training_prediction_model")
async def train_frozen_models(input_row = None): 
    try: 
        input_data = json.loads(input_row.json())
        session  = get_session({"ROW_STRING" : input_data})
        context  = get_context(session)
        catalog = context.catalog
        session.run(pipeline_name  = "train_model_predict", runner=SequentialRunner(is_async=True))
        return catalog.load("classifier")
    except Exception as e:
        # Log the error with the appropriate level and stack trace
        logger.error("An error occurred in train_model():", exc_info=True)
"""Project pipelines."""
from typing import Dict
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from forecast_weather.pipelines import data_processing as dp
from forecast_weather.pipelines import data_forecasting as df
from forecast_weather.pipelines import data_science as ds
from forecast_weather.pipelines import prediction_weather as pw

# from forecast_weather.pipelines import api_pipeline as api

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_preprocessing = dp.create_pipeline()
    forcasting = df.create_pipeline()
    modeling = ds.create_pipeline()
    proba_frozen = pw.create_pipeline()

    # api_pipeline = api.create_pipeline()
    
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values())

    train_model_frocast = data_preprocessing #+ forcasting

    pipelines["train_model_frocast"] = train_model_frocast
    pipelines["train_model_predict"] = modeling
    pipelines["proba_frozen"] = proba_frozen

    return pipelines
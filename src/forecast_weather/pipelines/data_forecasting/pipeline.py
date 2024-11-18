"""
This is a boilerplate pipeline 'data_forecasting'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import list__train_model_TS

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
          node(
                 list__train_model_TS,
                 ["df_forecast_input", "params:forecast_model_options"],
                 "dict_forecasting_model"
          )
        ]
    )

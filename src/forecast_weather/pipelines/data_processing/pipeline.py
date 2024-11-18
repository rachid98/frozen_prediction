"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import create_models_input_table


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
           node(
                create_models_input_table,
                ["weather_data", "params:threshold", "params:forecast_model_options", "params:alpha_outliers"],
                ["df_predict_input", "df_forecast_input"]      
           )
        ]
    )

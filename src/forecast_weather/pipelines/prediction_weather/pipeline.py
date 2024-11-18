"""
This is a boilerplate pipeline 'prediction_weather'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import prediction_weather, forecast_params_row, csv_generated

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(csv_generated,
             ["df_predict_input", "classifier", "predict_row_input","params:forecast_model_options", "params:model_options"],
             "csv_generated",
        ) 
    ]
)
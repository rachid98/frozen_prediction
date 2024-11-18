"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import evaluate_model, split_data, train_model

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                split_data,
                ["df_predict_input", "params:model_options"],
                ["X_train", "X_test", "y_train", "y_test", "X", "y"],
            ),
            node(
                train_model,
                ["X_train", "y_train", "params:model_options"],
                "classifier",
            ),
            node(
                evaluate_model,
                ["classifier", "X", "y"],
                None,
            ),
        ]
    )
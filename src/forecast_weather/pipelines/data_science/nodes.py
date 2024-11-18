"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.18.9
"""

import logging
from typing import Dict, Tuple

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, f1_score

##################################################################################################################
##################################################################################################################

def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["frozen_id"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"], stratify=y,
    )
    return X_train, X_test, y_train, y_test, X, y
##################################################################################################################
##################################################################################################################

def train_model(X_train: pd.DataFrame, y_train: pd.Series, parameters: Dict) -> XGBClassifier:
    """Trains the XGBClassifier model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    classifier = XGBClassifier(scale_pos_weight=parameters["scale_pos_weight"],
                          objective=parameters["objective"],
                          random_state=parameters["random_state"])
    classifier.fit(X_train, y_train)
    return classifier
##################################################################################################################
##################################################################################################################
def evaluate_model(
    classifier: XGBClassifier, X_test: pd.DataFrame, y_test: pd.Series
):
    """Calculates and logs the coefficient of determination.

    Args:
        classifier: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = classifier.predict(X_test)
    score = f1_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a f1 score of %.3f on test data.", score)
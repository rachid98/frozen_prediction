"""
This is a boilerplate pipeline 'data_forecasting'
generated using Kedro 0.18.9
"""
import logging
from typing import Dict, Tuple

import pandas as pd
from pmdarima import auto_arima

##################################################################################################################
##################################################################################################################

def train_model_TS(train_series: pd.Series, parameters: Dict):
    """Trains the ARIMA model.

    Args:
        train_series: Training data of independent features.
        parameters: Parameters defined in parameters/data_forecasting.yml.

    Returns:
        Trained model.
    """
    forecaster = auto_arima(train_series, seasonal=parameters["seasonal"], trace=parameters["trace"])
    model_fit = forecaster.fit(train_series)
    return model_fit
##################################################################################################################
##################################################################################################################

def list__train_model_TS(df_forecast: pd.DataFrame, parameters: Dict):
    dict_model = {}
    parameters["features"].remove("Date")
    for feature in parameters["features"] :
        train_series = df_forecast[feature]
        dict_model[feature] = train_model_TS(train_series, parameters)
    return dict_model


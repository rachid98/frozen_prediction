"""
This is a boilerplate pipeline 'prediction_weather'
generated using Kedro 0.18.9
"""
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import random
# random.seed()

def forecast_params_row(df_series, param_row, parameters):

    # last_date = df_series.index[-1]
    # target_date = pd.Timestamp(param_row["start_date"])
    # # forecast_periods = pd.date_range(start=param_row["start_date"], end=param_row["end_date"], freq='D')
    # forecast_steps =  (target_date - last_date).days # + len(forecast_periods)
    # focecast_dates = [last_date + timedelta(days=i) for i in range(1, forecast_steps + 1)]
    # parameters["features"].remove("Date")
    # for feature in parameters["features"]:
    #     forecast = foract_models[feature].predict(n_periods=forecast_steps)
    #     forecast.index = focecast_dates
    #     print(round(forecast[target_date],2))
    #     distances = np.abs(df_series[feature] - round(forecast[target_date],2))
    #     indice_valeur_proche = distances.idxmin()
    #     param_row[feature] = df_series.loc[indice_valeur_proche, feature]
    # print(df_series)
    # date_obj = datetime.strptime(param_row["start_date"][:-6], "%Y-%m-%d %H:%M:%S")
    # df_series.index = pd.to_datetime(df_series.index)
    # jour = date_obj.day
    # mois = date_obj.month
    # Extrait le jour et le mois de l'index
    # df_series['jour'] = df_series.index.day
    # df_series['mois'] = df_series.index.month
    df_series = df_series.astype({"month" : str, "department_code" : str})

    def select_lignes_groupe(groupe):
        return groupe[(groupe['department_code'] == str(param_row["department_code"])) & (groupe['month'] == str(param_row["start_date"]))]
    
    lignes_selectionnees = df_series.groupby(['department_code', 'department_code']).apply(select_lignes_groupe).reset_index(drop=True)
    probabilite = lignes_selectionnees["frozen_id"].sum() / len(lignes_selectionnees) 
    ligne_mediane = lignes_selectionnees[lignes_selectionnees["frozen_id"] == 1].reset_index(drop=True)
    ligne_mediane = ligne_mediane.astype({"month" : int, "department_code" : int})

    if ligne_mediane.empty:
        ligne_mediane = lignes_selectionnees[lignes_selectionnees["frozen_id"] == 0].reset_index(drop=True)
    ligne_mediane = ligne_mediane.astype({"month" : int, "department_code" : int})
    if "Date" in parameters["features"]:
        parameters["features"].remove("Date")
    for feature in parameters["features"]:
        param_row[feature] = round(ligne_mediane[feature].iloc[0],2)

    param_row = {key: value.item() if isinstance(value, np.int32) else value for key, value in param_row.items()}
    return param_row, probabilite

##################################################################################################################
##################################################################################################################

def prediction_weather(model_predic, params_row, parameters, probabilite):
    params_row = {key: [value] for key, value in params_row.items()}
    predic_row = pd.DataFrame(params_row)
    # predic_row["start_date"] = pd.to_datetime(predic_row["start_date"], utc=True)
    # predic_row['month'] = predic_row['start_date'].dt.strftime('%m')
    # predic_row['hour'] = predic_row['start_date'].dt.strftime('%H')
    predic_row = predic_row.astype({'start_date': int, 'department_code': int})

    colonnes_to_drop = [colonne for colonne in predic_row.columns if colonne not in parameters["features"]]
    predic_row = predic_row.drop(columns=colonnes_to_drop).reindex(columns=parameters["features"])
    predic_proba = abs(model_predic.predict_proba(predic_row)[0][1]*100)
    if predic_proba < 0.01:
      predic_proba += probabilite*100 + random.uniform(0.2,0.5)*100
    #   print("<0.01: ", predic_proba)
    else:
        predic_proba -= probabilite*100 + random.uniform(0, 0.3)*100
        # print(">0.01: ", predic_proba)
    return predic_proba

##################################################################################################################
##################################################################################################################

def csv_generated(df_series, model_predic, params_row, parameters1,parameters2 ):
     df_series = df_series.astype({"month" : str, "department_code" : str})
     months = df_series['month'].unique()
     departments = df_series['department_code'].unique()
     list_predict_2 = [departments]
     
     for month in months:
         list_predict_1 = []
         params_row["start_date"] = int(month)
         for deprtmnt in departments:
             params_row["department_code"] = int(deprtmnt)
             params_row, probabilite = forecast_params_row(df_series, params_row, parameters1)
             list_predict_1.append(prediction_weather(model_predic, params_row, parameters2, probabilite))
         list_predict_2.append(list_predict_1)
     mois = ['departement','janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']
     dict_values = {mois[i]: list_predict_2[i] for i in range(len(mois))}
     return pd.DataFrame(dict_values, index = departments)
 
    
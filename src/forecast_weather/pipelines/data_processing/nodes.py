"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.9
"""
import pandas as pd
import numpy as np
from unidecode import unidecode

def elements_existants(liste_plus_grande, liste_a_verifier):
    # Convertir les deux listes en ensembles
    ensemble_plus_grand = set(liste_plus_grande)
    ensemble_a_verifier = set(liste_a_verifier)

    # Vérifier si tous les éléments de la liste à vérifier existent dans la liste plus grande
    return ensemble_a_verifier.issubset(ensemble_plus_grand)

##################################################################################################################
##################################################################################################################

def nettoyer_nom(nom):
    # Remplacer les caractères spéciaux par des caractères non accentués et les espaces par des underscores
    nom = unidecode(nom)
    nom = nom.replace(' ', '_').replace('(', '').replace(')', '')
    return nom

def selected_feature(df, threshold):
    lst_not_drop = ["Point_de_rosee", "Humidite", "Visibilite_horizontale", "Rafales_sur_une_periode", "department_code", "Date", "Temperature_degC" ]
    names_col = []

    missing_percentage = (df.isnull().sum() / len(df)) * 100
    columns_to_drop = missing_percentage[missing_percentage > threshold].index
    df_cleaned = df.drop(columns=columns_to_drop)
    for d in df_cleaned.columns:
        names_col.append(nettoyer_nom(d))
    dict_drop = {df_cleaned.columns[i] : names_col[i] for i in range(len(df_cleaned.columns)) }
    df_cleaned.rename(columns = dict_drop, inplace = True)

    for d in df_cleaned.columns:
       if d not in lst_not_drop:
            df_cleaned = df_cleaned.drop(columns=[d])
    # nouveaux_noms = [nettoyer_nom(col) for col in df_cleaned.columns]
    # df_cleaned = df_cleaned.rename(columns=dict(zip(df_cleaned.columns, nouveaux_noms)))
    return df_cleaned

##################################################################################################################
##################################################################################################################

def preprocess_date(df_cleaned):
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], utc=True)
    df_cleaned['month'] = df_cleaned['Date'].dt.strftime('%m')
    df_cleaned['hour'] = df_cleaned['Date'].dt.strftime('%H')
    df_cleaned = df_cleaned.astype({'month': int, 'hour': int})
    return df_cleaned.sort_values(by = 'Date', ascending=False)
##################################################################################################################
##################################################################################################################
def remove_outliers(df_chro, alpha):
    """
    Removes outliers from a DataFrame using Tukey's method.

    Args:
        df (DataFrame): The DataFrame containing the data.
        alpha (float): The Tukey coefficient (default is 1.5).

    Returns:
        DataFrame: The DataFrame with outliers removed.
    """
    df_clean = df_chro.copy()

    for col in df_chro.columns:
        #Takes two parameters: dataframe & variable of interest as string
        q1 = df_chro[col].quantile(0.25)
        q3 = df_chro[col].quantile(0.75)
        iqr = q3-q1
        inner_fence = alpha*iqr
        #inner fence lower and upper end
        inner_fence_le = q1-inner_fence
        inner_fence_ue = q3+inner_fence
        # remove outliers
        df_clean = df_clean[(df_clean[col] >= inner_fence_le) & (df_clean[col] <= inner_fence_ue)]
        return df_clean
##################################################################################################################
##################################################################################################################

def new_feature(df_cleaned):
    df_cleaned['frozen_id'] = df_cleaned['Temperature_degC'].apply(lambda x: 1 if x <= 0 else 0)
    df_cleaned = df_cleaned.drop(columns = ['Temperature_degC'])
    return df_cleaned
##################################################################################################################
##################################################################################################################

def preprocess_missing_value(df_cleaned):
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
    df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(df_cleaned[numeric_columns].median())
    # df_cleaned[categorical_columns] = df_cleaned[categorical_columns].fillna(df_cleaned[categorical_columns].mode().iloc[0])
    return df_cleaned
##################################################################################################################
##################################################################################################################

def preprocess_time_series(df_cleaned, parameters):
    series = df_cleaned.loc[:, parameters["features"]]
    series.set_index('Date', inplace=True)
    daily_median = series.resample('D').last()
    return daily_median
##################################################################################################################
##################################################################################################################

def create_models_input_table(df, threshold, parameters, alpha):
    df_cleaned = selected_feature(df, threshold)
    df_cleaned = preprocess_date(df_cleaned)
    df_cleaned = new_feature(df_cleaned)
    predict_input_table = preprocess_missing_value(df_cleaned)
    forecast_input_table = preprocess_time_series(predict_input_table, parameters)
    forecast_input_table = remove_outliers(forecast_input_table, alpha)
    predict_input_table.drop(columns = ['hour'], inplace = True)
    return predict_input_table, forecast_input_table



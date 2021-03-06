import pandas as pd
import numpy as np
import datetime
from getting_started import *
import detect_duplicates_script as script_dd

# Dans cette fonction on corrige les anomalies de la colonne 'pcr'
def get_cleaned_df_pcr(data):
    df_pcr_cleaned = df_pcr.copy()
    # On commence par changer le type de la colonne 'postcode' en string
    df_pcr_cleaned.loc[:,'pcr']= df_pcr_cleaned['pcr'].astype(str)
    # On supprime les espaces avant et après 
    df_pcr_cleaned.loc[:,'pcr'] = df_pcr_cleaned['pcr'].str.strip()
    # Conversion en majuscule 
    df_pcr_cleaned.loc[:,'pcr'] = df_pcr_cleaned['pcr'].str.upper()
    # Normalisation de la colonne pcr
    # 'negative' <=== 0 
    df_pcr_cleaned["pcr"].replace({"N": 0}, inplace=True)
    df_pcr_cleaned["pcr"].replace({"NEGATIVE": 0}, inplace=True)
    # 'postive' <=== 1
    df_pcr_cleaned["pcr"].replace({"P": 1}, inplace=True)
    df_pcr_cleaned["pcr"].replace({"POSITIVE": 1}, inplace=True)
    #
    return df_pcr_cleaned
    

# Dans cette fonction on finalise notre processus de nettoyage de données. 
def get_final_ds(data_patient, data_pcr, path_referential):
    
    # data frame obtenu après suppression des duplications du jeu de donnée patient
    df_patient_dedup = script_dd.detect_duplicates(data_patient, path_referential)
    
    # data frame obtenu après un processus de data cleaning appliqué au jeu de données
    # sur les données relatifs aux contamination par le Covid19
    df_cleaned_pcr = get_cleaned_df_pcr(data_pcr)
    # On fusionne les dataframes de patients (dédupliquée) avec celle des résultats des test du Covid19
    df_final_ds = pd.merge(df_cleaned_pcr,
                           df_patient_dedup,
                           on='patient_id', 
                           how='left')
    
    # Pour fiabiliser notre analyse statistique, nous éliminons toutes les lignes
    # avec des valeurs manquantes ou érronées sur l'une des colonnes : 
    # date_of_birth, postcode et patient_id.
    # (Rappelons que dans cette exemple toutes les valeurs de patient_id sont valides)
    df_final_ds = df_final_ds[df_final_ds['patient_id'].notnull() 
                              & df_final_ds['date_of_birth'].notnull() 
                              & df_final_ds['postcode'].notnull() 
                              & df_final_ds['postcode'] != 0]
    # Supprimer les lignes avec des valeurs inconnues au niveau de 'state'
    df_final_ds = df_final_ds[df_final_ds['state'] != "UNKNOWN"]
    
    return df_final_ds
    
    






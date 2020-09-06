# 
# pip install -U pytest
# pip install pandas -U

import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from detect_duplicates_script import detect_duplicates
import datetime

def test_delete_duplicates():
    
    df = pd.DataFrame([
        [771155, 4210, 'QL', 19790108, np.nan],
        [771155, 'null', 'nsss', 19991892.0, 'age of the patient'],
        [771155, '4210', 'nsss', np.nan, 32]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df)
    
    df_expected = pd.DataFrame([
        [771155, 4210, 'QLD', datetime.datetime.strptime('1979-01-08', '%Y-%m-%d'), 41]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    #df_expected.loc[:,'patient_id'] = df_expected['patient_id'].astype(int)
    #df_expected.loc[:,'postcode'] = df_expected['postcode'].astype(int)
    #df_expected.loc[:,'state'] = df_expected['state'].astype(str)
    #df_expected.loc[:,'age'] = df_expected['age'].astype(float)
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)


def test_correct_age():
        
    df = pd.DataFrame([
        [100064, 4208, 'QLD', 19810905.0, np.nan],
        [100215, 6107, 'WA', 19061018.0, ''],
        [100363, 3029, 'VIC', 19030606.0, 32]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    df_result = detect_duplicates(df)
    
    df_expected = pd.DataFrame([
        [100064, 4208, 'QLD', datetime.datetime.strptime('1981-09-05', '%Y-%m-%d'), 39],
        [100215, 6107, 'WA', datetime.datetime.strptime('1906-10-18', '%Y-%m-%d') , 114],
        [100363, 3029, 'VIC', datetime.datetime.strptime('1903-06-06', '%Y-%m-%d'), 117]
        ], columns = ['patient_id', 'postcode', 'state', 'date_of_birth', 'age'])
    
    assert_frame_equal(left=df_expected.reset_index(drop=True), right=df_result.reset_index(drop=True),
                       check_dtype=False)                   
                       
        
        
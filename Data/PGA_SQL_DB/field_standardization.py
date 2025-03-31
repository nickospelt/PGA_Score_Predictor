from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import sqlite3

# main function to control control
if __name__ == "__main__":
    # connect to the database
    conn = sqlite3.connect('/Users/nickospelt/Documents/App_Projects/PGA_Score_Predictor/Data/PGA_SQL_DB/PGA.db')
    
    # pull ewa metrics
    ewa_metrics_df = pd.read_sql_query("SELECT * FROM EWA_METRICS", conn)


    # Features Want to Standardize
    ['HL_50_SG_P', 'HL_100_SG_P', 'HL_200_SG_P',
        'HL_50_SG_OTT', 'HL_100_SG_OTT', 'HL_200_SG_OTT',
        'HL_50_SG_APR', 'HL_100_SG_APR', 'HL_200_SG_APR',
        'HL_50_SG_ATG', 'HL_100_SG_ATG', 'HL_200_SG_ATG',
        'HL_50_R1_SCR', 'HL_100_R1_SCR', 'HL_200_R1_SCR',
        'HL_50_R2_SCR', 'HL_100_R2_SCR', 'HL_200_R2_SCR',
        'HL_50_R3_SCR', 'HL_100_R3_SCR', 'HL_200_R3_SCR',
        'HL_50_R4_SCR', 'HL_100_R4_SCR', 'HL_200_R4_SCR', 
        'T12_EARNINGS', 'T12_FED_EX_PTS', 
        'T12_WINS', 'T12_TOP_5', 'T12_TOP_10', 'T12_TOP_20', 
        'T12_MADE_CUTS', 'T12_APPERANCES']

    # save to a table in database
    #standardized_metrics_df.to_sql('STANDARDIZED_METRICS', conn, if_exists='replace', index=False)
    
    conn.close()
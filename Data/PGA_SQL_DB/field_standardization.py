from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import sqlite3

# standardized features based on other players in the field and clean values that are null
def standardize_feature_distributions(ewa_metrics_df, tournament_df, tournament_name, player_name, tournament_date, finish, features):
    player_df = ewa_metrics_df.loc[(ewa_metrics_df['TOURNAMENT_NAME'] == tournament_name) & (ewa_metrics_df['PLAYER_NAME'] == player_name)]

    if (len(player_df) != 1):
        raise ValueError("Should only be one row for the player and tournament group")

    results = []
    results.append(tournament_name)
    results.append(player_name)
    results.append(tournament_date)
    results.append(finish)

    for feature in features:
        orig_val = player_df[feature].iloc[0]

        standardized_feature = 0
        if not pd.isnull(orig_val):
            if feature != 'POSITION':
                mean = tournament_df.loc[tournament_name, (feature, 'mean')]
                std = tournament_df.loc[tournament_name, (feature, 'std')]

                if feature[:3] != "T12" and std == 0:
                    print(tournament_name, feature)
                    raise ValueError("Zero STD")
                elif std == 0:
                    standardized_feature = orig_val
                else:
                    standardized_feature = (orig_val - mean) / std
            else:
                min_val = tournament_df.loc[tournament_name, (feature, 'min')]
                max_val = tournament_df.loc[tournament_name, (feature, 'max')]
                
                standardized_feature = (orig_val - min_val) / (max_val - min_val)
        elif feature == 'POSITION':
            standardized_feature = -1

        results.append(standardized_feature)
    
    return results

# main function to control control
if __name__ == "__main__":
    # connect to the database
    conn = sqlite3.connect('/Users/nickospelt/Documents/App_Projects/PGA_Tournament_Winner/Data/PGA_SQL_DB/PGA.db')
    
    # pull ewa metrics
    ewa_metrics_df = pd.read_sql_query("SELECT * FROM EWA_METRICS", conn)

    # features
    # Features Want to Standardize
    features = ['POSITION',
        'HL_50_SG_P', 'HL_100_SG_P', 'HL_200_SG_P',
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
    
    # calculate average and std for all features for each tournament
    tournament_df = pd.DataFrame()
    tournament_df = ewa_metrics_df.groupby('TOURNAMENT_NAME')[features].agg(['mean', 'std', 'min', 'max'])

    standardized_metrics_df = pd.DataFrame()
    standardized_metrics_df[['TOURNAMENT_NAME', 'PLAYER_NAME', 'TOURNAMENT_DATE', 'FINISH', 'STANDARD_POSITION',
        'HL_50_SG_P', 'HL_100_SG_P', 'HL_200_SG_P',
        'HL_50_SG_OTT', 'HL_100_SG_OTT', 'HL_200_SG_OTT',
        'HL_50_SG_APR', 'HL_100_SG_APR', 'HL_200_SG_APR',
        'HL_50_SG_ATG', 'HL_100_SG_ATG', 'HL_200_SG_ATG',
        'HL_50_R1_SCR', 'HL_100_R1_SCR', 'HL_200_R1_SCR',
        'HL_50_R2_SCR', 'HL_100_R2_SCR', 'HL_200_R2_SCR',
        'HL_50_R3_SCR', 'HL_100_R3_SCR', 'HL_200_R3_SCR',
        'HL_50_R4_SCR', 'HL_100_R4_SCR', 'HL_200_R4_SCR', 
        'T12_EARNINGS', 'T12_FED_EX_PTS', 
        'T12_WINS', 'T12_TOP_5', 'T12_TOP_10', 'T12_TOP_20', 
        'T12_MADE_CUTS', 'T12_APPERANCES']] = ewa_metrics_df.apply(
        lambda row: pd.Series(
            standardize_feature_distributions(ewa_metrics_df, tournament_df,
                row['TOURNAMENT_NAME'], row['PLAYER_NAME'], row['TOURNAMENT_DATE'], row['FINISH'], features)), axis=1)

    #print(standardized_metrics_df)

    # save to a table in database
    standardized_metrics_df.to_sql('STANDARDIZED_METRICS', conn, if_exists='replace', index=False)
    
    conn.close()
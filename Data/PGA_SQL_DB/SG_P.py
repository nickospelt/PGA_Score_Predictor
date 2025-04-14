from datetime import datetime, timedelta
from re import T
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import sqlite3

# Historical Strokes Gained Putting Values to Capture
# last 5 ADJ_SG_P values and days since each
# last 5 SG_PUTT values and days since each
# T_5 Event Average
# T_12 month ADJ_SG_P Average
# T_12 month SG_PUTT Average
# STD(ADJ_SG_P)
# STD(SG_PUTT)
# T_12 Cuts Made (or SG_PUTT values)
# Targets:
    # ADJ_SG_P
    # SG_PUTT


def convert_string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

def compute_days_between(date_one, date_two):
    duration = date_two - date_one
    return duration.days

# calculate requested strokes gained putting stats from above
def calc_sg_p_values(df, tournament_name, player_name, tournament_date, sg_p, adj_sg_p, position):
    prev_year_date = tournament_date - relativedelta(days=369)
    df = df.loc[(df['PLAYER_NAME'] == player_name) & (df['TOURNAMENT_DATE'] < tournament_date)].copy()

    if df.shape[0] == 0:
        return tournament_name, player_name, tournament_date, sg_p, adj_sg_p, position, None
    
    # capture all apperances (wether made the cut of not in the last 12 months)
    t12_apperances = df.loc[df['TOURNAMENT_DATE'] > prev_year_date].shape[0]

    # prepare data to get valid strokes gained putt data
    df['DAYS_SINCE'] = df.apply(lambda row: compute_days_between(row['TOURNAMENT_DATE'], tournament_date), axis=1)
    df = df.dropna()

    # return data for the current tournament
    results = []
    results.append(tournament_name)
    results.append(player_name)
    results.append(tournament_date)
    results.append(sg_p)
    results.append(adj_sg_p)
    results.append(position)

    # calculate and record the standard deviations of adjusted strokes gained putting and strokes gained putting for that player
    std_adj_sg_p = df['ADJ_SG_P'].std()
    std_sg_p = df['SG_PUTT'].std()

    results.append(std_adj_sg_p)
    results.append(std_sg_p)

    # record previous 5 strokes gained putting metrics
    for idx in range(5):
        try:
            ADJ_SG_P_N, SG_P_N, DAYS_N = df[['ADJ_SG_P', 'SG_PUTT', 'DAYS_SINCE']].iloc[idx]
        except IndexError:
            ADJ_SG_P_N, SG_P_N, DAYS_N = None, None, None

        results.append(ADJ_SG_P_N)
        results.append(SG_P_N)
        results.append(DAYS_N)

    # calculate the average of the non-null strokes gained values from last 5 tournaments
    t5_avg_adj_sg_p = results[8]
    t5_avg_sg_p = results[9]
    if df.shape[0] >= 5:
        t5_avg_adj_sg_p = (results[8] + results[11] + results[14] + results[17] + results[20]) / 5
        t5_avg_sg_p = (results[9] + results[12] + results[15] + results[18] + results[21]) / 5
    elif df.shape[0] == 4:
        t5_avg_adj_sg_p = (results[8] + results[11] + results[14] + results[17]) / 4
        t5_avg_sg_p = (results[9] + results[12] + results[15] + results[18]) / 4
    elif df.shape[0] == 3:
        t5_avg_adj_sg_p = (results[8] + results[11] + results[14]) / 3
        t5_avg_sg_p = (results[9] + results[12] + results[15]) / 3
    elif df.shape[0] == 2:
        t5_avg_adj_sg_p = (results[8] + results[11]) / 2
        t5_avg_sg_p = (results[9] + results[12]) / 2
    
    results.append(t5_avg_adj_sg_p)
    results.append(t5_avg_sg_p)

    # calculate trailing 12 month strokes gained data    
    df = df.loc[df['TOURNAMENT_DATE'] > prev_year_date]

    t12_sg_putt = df.shape[0]
    t12_avg_adj_sg_p = df['ADJ_SG_P'].mean()
    t12_avg_sg_p = df['SG_PUTT'].mean()

    results.append(t12_avg_adj_sg_p)
    results.append(t12_avg_sg_p)
    results.append(t12_sg_putt)
    results.append(t12_apperances)

    return results

# main function to control control
if __name__ == "__main__":
    # connect to the database
    conn = sqlite3.connect('/Users/nickospelt/Documents/App_Projects/PGA_Tournament_Winner/Data/PGA_SQL_DB/PGA.db')
    
    # pull adjusted metrics
    sg_p_query = """WITH
        RAW_SG_P AS (
            SELECT TOURNAMENT_NAME, TOURNAMENT_DATE, PLAYER_NAME, SG_PUTT, POSITION
            FROM RAW_TOURNAMENT_ROUNDS_V5
        ),
        ADJUSTED_SG_P AS (
            SELECT TOURNAMENT_NAME, TOURNAMENT_DATE, PLAYER_NAME, ADJ_SG_P
            FROM ADJ_METRICS
        )

        SELECT RAW_SG_P.TOURNAMENT_NAME, RAW_SG_P.TOURNAMENT_DATE, RAW_SG_P.PLAYER_NAME, SG_PUTT, ADJ_SG_P, POSITION
        FROM RAW_SG_P INNER JOIN ADJUSTED_SG_P 
            ON RAW_SG_P.TOURNAMENT_NAME = ADJUSTED_SG_P.TOURNAMENT_NAME
            AND RAW_SG_P.PLAYER_NAME = ADJUSTED_SG_P.PLAYER_NAME
        ORDER BY RAW_SG_P.PLAYER_NAME, RAW_SG_P.TOURNAMENT_DATE DESC
    """
    raw_sg_p_df = pd.read_sql_query(sg_p_query, conn)
    raw_sg_p_df['TOURNAMENT_DATE'] = raw_sg_p_df.apply(lambda row: convert_string_to_date(row['TOURNAMENT_DATE']), axis=1)

    # compute the exponentially weighted values
    sg_p_df = pd.DataFrame()
    sg_p_df[['TOURNAMENT_NAME', 'PLAYER_NAME', 'TOURNAMENT_DATE', 'ADJ_SG_P', 'SG_P', 'POSITION',
        'STD_ADJ_SG_P', 'STD_SG_P', 
        'ADJ_SG_P_1', 'SG_P_1', 'DAYS_1',
        'ADJ_SG_P_2', 'SG_P_2', 'DAYS_2',
        'ADJ_SG_P_3', 'SG_P_3', 'DAYS_3',
        'ADJ_SG_P_4', 'SG_P_4', 'DAYS_4',
        'ADJ_SG_P_5', 'SG_P_5', 'DAYS_5',
        'T5_AVG_ADJ_SG_P', 'T5_AVG_SG_P',
        'T12_AVG_ADJ_SG_P', 'T12_AVG_SG_P',
        'T12_SG_PUTT', 'T12_APPERANCES']] = raw_sg_p_df.apply(
        lambda row: pd.Series(
            calc_sg_p_values(raw_sg_p_df, 
                row['TOURNAMENT_NAME'], row['PLAYER_NAME'], row['TOURNAMENT_DATE'], row['SG_PUTT'], row['ADJ_SG_P'], row['POSITION'])), axis=1)

    # save to a table in database
    sg_p_df.to_sql('SG_P_EDA', conn, if_exists='replace', index=False)
    
    conn.close()

from datetime import datetime, timedelta
from re import T
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import sqlite3

def convert_string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

def compute_days_between(date_one, date_two):
    duration = date_two - date_one
    return duration.days

def compute_half_life_weight(half_life, days):
    return np.power(0.5, (days / half_life))

# for each row, need to look at all previous tournaments for that player. and calculate weights based on the different between that rows tournament date and the other rows tournament weight.
def calc_weighted_avgs(df, tournament_name, player_name, tournament_date, features):
    # only interested in historical rows and anything greater than 1329 days ago will have an insignificant weight
    #  & (df['TOURNAMENT_DATE'] >= (tournament_date - timedelta(days=1329)
    prev_rounds_df = df.loc[(df['PLAYER_NAME'] == player_name) & (df['TOURNAMENT_DATE'] < tournament_date)].copy()

    # determine if eligible rows
    if prev_rounds_df.shape[0] == 0:
        return tournament_name, player_name, tournament_date, None
    
    # Weighting by how recent data is
    prev_rounds_df['DAYS_SINCE'] = prev_rounds_df.apply(lambda row: compute_days_between(row['TOURNAMENT_DATE'], tournament_date), axis=1)
    prev_rounds_df['HL_50_WEIGHT'] = prev_rounds_df.apply(lambda row: compute_half_life_weight(50, row['DAYS_SINCE']), axis=1)
    prev_rounds_df['HL_100_WEIGHT'] = prev_rounds_df.apply(lambda row: compute_half_life_weight(100, row['DAYS_SINCE']), axis=1)
    prev_rounds_df['HL_200_WEIGHT'] = prev_rounds_df.apply(lambda row: compute_half_life_weight(200, row['DAYS_SINCE']), axis=1)
    
    # generate half life values based on previous rounds
    # calculate ewa metric (therefore weights) only for when that feature is not null
    hl_values = []
    for feature in features:
        poss_values = prev_rounds_df[feature].unique().tolist()

        # if no previous values for the metric then null for all half-lifes
        if len(poss_values) == 1 and np.isnan(poss_values[0]):
            hl_values.append(None)
            hl_values.append(None)
            hl_values.append(None)
        else:
            fifty = "HL_50_" + feature
            hundred = "HL_100_" + feature
            two_hundred = "HL_200_" + feature

            # only consider tournaments where that player had a value for the specified feature
            feature_df = prev_rounds_df[prev_rounds_df[feature].notna()]

            weight_sum_HL_50 = feature_df['HL_50_WEIGHT'].sum()
            weight_sum_HL_100 = feature_df['HL_100_WEIGHT'].sum()
            weight_sum_HL_200 = feature_df['HL_200_WEIGHT'].sum()


            # compute weighted feature
            feature_df[fifty] = feature_df['HL_50_WEIGHT'] * feature_df[feature]
            feature_df[hundred] = feature_df['HL_100_WEIGHT'] * feature_df[feature]
            feature_df[two_hundred] = feature_df['HL_200_WEIGHT'] * feature_df[feature]

            fifty = feature_df[fifty].sum() / weight_sum_HL_50
            hundred = feature_df[hundred].sum() / weight_sum_HL_100
            two_hundred = feature_df[two_hundred].sum() / weight_sum_HL_200

            hl_values.append(fifty)
            hl_values.append(hundred)
            hl_values.append(two_hundred)

    return tournament_name, player_name, tournament_date, hl_values[0], hl_values[1], hl_values[2], hl_values[3], hl_values[4], hl_values[5], hl_values[6], hl_values[7], hl_values[8], hl_values[9], hl_values[10], hl_values[11], hl_values[12], hl_values[13], hl_values[14], hl_values[15], hl_values[16], hl_values[17], hl_values[18], hl_values[19],  hl_values[20], hl_values[21], hl_values[22], hl_values[23]

# for tournaments within the past 12 months, compute the players finish statistics
def calc_yearly_finish_totals(df, player_name, tournament_name, tournament_date, finish, position):
    prev_year_date = tournament_date - relativedelta(days=369)
    prev_year_rounds_df = df[['TOURNAMENT_DATE', 'EARNINGS', 'FEDEX_PTS', 'FINISH']].loc[(df['PLAYER_NAME'] == player_name) & (df['TOURNAMENT_DATE'] < tournament_date) & (df['TOURNAMENT_DATE'] >= prev_year_date)].copy()

    if prev_year_rounds_df.shape[0] == 0:
        return player_name, tournament_name, finish, position, 0, 0, 0, 0, 0, 0, 0, 0

    # all metrics at an per apperance level
    apperances = prev_year_rounds_df.shape[0]
    earnings = prev_year_rounds_df['EARNINGS'].sum() / apperances
    fed_ex_pts = prev_year_rounds_df['FEDEX_PTS'].sum() / apperances
    wins = (prev_year_rounds_df['FINISH'] == 'WIN').sum() / apperances
    top_five = ((prev_year_rounds_df['FINISH'] == 'WIN') | (prev_year_rounds_df['FINISH'] == 'TOP 5')).sum() / apperances
    top_ten = ((prev_year_rounds_df['FINISH'] == 'WIN') | (prev_year_rounds_df['FINISH'] == 'TOP 5') | (prev_year_rounds_df['FINISH'] == 'TOP 10')).sum() / apperances
    top_twenty = ((prev_year_rounds_df['FINISH'] == 'WIN') | (prev_year_rounds_df['FINISH'] == 'TOP 5') | (prev_year_rounds_df['FINISH'] == 'TOP 10') | (prev_year_rounds_df['FINISH'] == 'TOP 20')).sum() / apperances
    made_cuts = ((prev_year_rounds_df['FINISH'] == 'WIN') | (prev_year_rounds_df['FINISH'] == 'TOP 5') | (prev_year_rounds_df['FINISH'] == 'TOP 10') | (prev_year_rounds_df['FINISH'] == 'TOP 20') | (prev_year_rounds_df['FINISH'] == 'MADE CUT')).sum() / apperances

    return player_name, tournament_name, finish, position, earnings, fed_ex_pts, wins, top_five, top_ten, top_twenty, made_cuts, apperances

# main function to control control
if __name__ == "__main__":
    # connect to the database
    conn = sqlite3.connect('/Users/nickospelt/Documents/App_Projects/PGA_Tournament_Winner/Data/PGA_SQL_DB/PGA.db')
    
    # pull adjusted metrics
    adj_metrics_df = pd.read_sql_query("SELECT * FROM ADJ_METRICS", conn)
    adj_metrics_df['TOURNAMENT_DATE'] = adj_metrics_df.apply(lambda row: convert_string_to_date(row['TOURNAMENT_DATE']), axis=1)

    # compute the exponentially weighted values
    ewa_metrics_df = pd.DataFrame()
    ewa_metrics_df[['TOURNAMENT_NAME', 'PLAYER_NAME', 'TOURNAMENT_DATE',
        'HL_50_SG_P', 'HL_100_SG_P', 'HL_200_SG_P',
        'HL_50_SG_OTT', 'HL_100_SG_OTT', 'HL_200_SG_OTT',
        'HL_50_SG_APR', 'HL_100_SG_APR', 'HL_200_SG_APR',
        'HL_50_SG_ATG', 'HL_100_SG_ATG', 'HL_200_SG_ATG',
        'HL_50_R1_SCR', 'HL_100_R1_SCR', 'HL_200_R1_SCR',
        'HL_50_R2_SCR', 'HL_100_R2_SCR', 'HL_200_R2_SCR',
        'HL_50_R3_SCR', 'HL_100_R3_SCR', 'HL_200_R3_SCR',
        'HL_50_R4_SCR', 'HL_100_R4_SCR', 'HL_200_R4_SCR']] = adj_metrics_df.apply(
        lambda row: pd.Series(
            calc_weighted_avgs(adj_metrics_df, 
                row['TOURNAMENT_NAME'], row['PLAYER_NAME'], row['TOURNAMENT_DATE'], 
                ["ADJ_SG_P","ADJ_SG_OTT", "ADJ_SG_APR", "ADJ_SG_ATG", "ADJ_R1_SCR", "ADJ_R2_SCR", "ADJ_R3_SCR", "ADJ_R4_SCR"])), axis=1)

    # compute trailing 12 month finish totals
    finish_df = pd.DataFrame()
    finish_df[['PLAYER_NAME', 'TOURNAMENT_NAME', 'FINISH', 'POSITION',
        'T12_EARNINGS', 'T12_FED_EX_PTS', 
        'T12_WINS', 'T12_TOP_5', 'T12_TOP_10', 'T12_TOP_20', 'T12_MADE_CUTS', 'T12_APPERANCES']] = adj_metrics_df.apply(
        lambda row: pd.Series(
            calc_yearly_finish_totals(adj_metrics_df, row['PLAYER_NAME'], row['TOURNAMENT_NAME'], row['TOURNAMENT_DATE'], row['FINISH'], row['POSITION'])), axis=1)

    # save to a table in database
    ewa_metrics_df = pd.merge(ewa_metrics_df, finish_df, on=['PLAYER_NAME', 'TOURNAMENT_NAME'], how='inner').sort_values(by=['TOURNAMENT_NAME', 'PLAYER_NAME'], ascending=[False, True])
    ewa_metrics_df.to_sql('EWA_METRICS', conn, if_exists='replace', index=False)
    
    conn.close()

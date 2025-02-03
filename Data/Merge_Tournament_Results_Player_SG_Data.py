import os
from pickle import FALSE, TRUE
import pandas as pd

# This file works the same way as Merge_Tournament_Results_Player_Data.py but accounts for the updated SG statistics

# Convert proximity to hole averages from a string format to a numerical format
def format_prox_to_hole(value):
    feet = int(value.split("'")[0])
    inch = int(value.split("\"")[0].split(" ")[1])
    return round(feet + (inch / 12), 4)

# Aggregate all player statistics for each individual player. Join that data with how each player played at the respective tournament
def aggregate_player_sg_and_tournament_data():
    main_dir = os.path.dirname(__file__)

    # list of all the tournament_player_data to be aggregated into final large data set
    master_tournament_player_data_df = pd.DataFrame(columns=["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", 
        "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", 
        "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH",
        'PLAYER_ID', 'PLAYER_NAME', 'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN',
        "SCORE", "TOTAL_SCORE"])

    # repeat this process for each tournament result file
    for tournament_result_csv in os.listdir(os.path.join(main_dir, 'Tournament_Results')):
        tournament_result_df = pd.read_csv(f"{os.path.join(main_dir, 'Tournament_Results')}/{tournament_result_csv}")
        
        # load and combine all player statistics (Commented out statistics not longer being used)
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}/Final Player Stats")
        
        try:
            SG_T2G_df = pd.read_csv(f'{player_data_path}/SG_T2G.csv')
        except FileNotFoundError:
            continue

        try:
            SG_PUTT_df = pd.read_csv(f'{player_data_path}/SG_PUTT.csv')
        except FileNotFoundError:
            continue


        # reformat data
        #prox_to_hole_df['AVG'] = prox_to_hole_df.apply(lambda x: format_prox_to_hole(x['AVG']), axis=1)

        # merge the player statistic dataframes together and format the final dataframe
        main_player_data_df = pd.merge(SG_T2G_df, SG_PUTT_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_x', 'TOTAL SG:PUTTING', 'SG:OTT', 'SG:APR', 'SG:ARG']].rename(columns={'PLAYER_x': 'PLAYER_NAME', 'TOTAL SG:PUTTING': 'SG_PUTT', 'SG:OTT': 'SG_OFF_THE_TEE', 'SG:APR': 'SG_APPROACH', 'SG:ARG': 'SG_AROUND_THE_GREEN'})
        main_player_data_df['SG_PUTT'] = main_player_data_df['SG_PUTT'] / 4

        # reorder the columns
        main_player_data_df['TOURNAMENT_NAME'] = tournament_result_csv.replace('.csv', '')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'TOURNAMENT_NAME', 'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN']]

        # print and save the aggregated player data for the respective tournament
        print(f"{tournament_result_csv.replace('.csv', '')} Player Stats Dataframe:")
        print(main_player_data_df)
        print('\n')
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}")
        main_player_data_df.to_csv(f"{os.path.join(player_data_path, 'main_player_data.csv')}", index=False)

        tournament_player_data_df = pd.merge(main_player_data_df, tournament_result_df, on=['PLAYER_NAME', 'TOURNAMENT_NAME']).sort_values(by='TOTAL_SCORE', ascending=False).reset_index(drop=True)
        tournament_player_data_df = tournament_player_data_df[["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", 
            "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", 
            "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH",
            'PLAYER_ID', 'PLAYER_NAME', 'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN',
            "SCORE", "TOTAL_SCORE"]]

        print(f"{tournament_result_csv.replace('.csv', '')} Final Dataframe:")
        print(tournament_player_data_df)
        print('\n')

        # add to the master dataset
        master_tournament_player_data_df = (
            pd.concat([master_tournament_player_data_df, tournament_player_data_df])
                .sort_values(by=['TOURNAMENT_NAME', 'TOTAL_SCORE', 'PLAYER_NAME', 'ROUND_DATE'], ascending=[False, True, True, False])
                .reset_index(drop=True)
        )
    print(f"Master Dataframe:")
    print(master_tournament_player_data_df)
    master_tournament_player_data_df.to_csv(f"{os.path.join(main_dir, 'master_pga_dataset.csv')}", index=False)

if __name__ == "__main__":
    aggregate_player_sg_and_tournament_data()
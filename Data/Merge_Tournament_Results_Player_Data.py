import os
from pickle import FALSE, TRUE
import pandas as pd

# Convert proximity to hole averages from a string format to a numerical format
def format_prox_to_hole(value):
    feet = int(value.split("'")[0])
    inch = int(value.split("\"")[0].split(" ")[1])
    return round(feet + (inch / 12), 4)

# Aggregate all player statistics for each individual player. Join that data with how each player played at the respective tournament
def aggregate_player_and_tournament_data():
    main_dir = os.path.dirname(__file__)

    # list of all the tournament_player_data to be aggregated into final large data set
    """master_tournament_player_data_df = pd.DataFrame(columns=["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH", "COURSE_AVERAGE_SCORE", 'PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 
    'AVG_PROX_TO_HOLE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', 'SCRAMBLING_PERCENTAGE', 'AVG_THREE_PUTTS_PER_ROUND', 'AVG_PUTTS_PER_ROUND', 
    "SCORE", "TOTAL_SCORE"])"""
    master_tournament_player_data_df = pd.DataFrame(columns=["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", 
        "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", 
        "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH", "R1_AVG_SCORE", "R2_AVG_SCORE", "R3_AVG_SCORE", "R4_AVG_SCORE", 
        'PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCRAMBLING_PERCENTAGE', 'PUTTS_PER_ROUND', 'R1_PUTTS',
        "SCORE", "TOTAL_SCORE"])

    # repeat this process for each tournament result file
    for tournament_result_csv in os.listdir(os.path.join(main_dir, 'Tournament_Results')):
        tournament_result_df = pd.read_csv(f"{os.path.join(main_dir, 'Tournament_Results')}/{tournament_result_csv}")
        
        # load and combine all player statistics (Commented out statistics not longer being used)
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}/Final_Player_Stats")
        gir_percentage_df = pd.read_csv(f'{player_data_path}/gir_percentage.csv')
        # birdie_to_bogey_ratio_df = pd.read_csv(f'{player_data_path}/birdie_to_bogey_ratio.csv')
        total_driving_distance_df = pd.read_csv(f'{player_data_path}/total_driving_distance.csv')
        fir_percentage_df = pd.read_csv(f'{player_data_path}/fir_percentage.csv')
        # scoring_average_df = pd.read_csv(f'{player_data_path}/scoring_average.csv')
        scrambling_percentage_df = pd.read_csv(f'{player_data_path}/scrambling_percentage.csv')
        # three_putts_per_round_df = pd.read_csv(f'{player_data_path}/three_putts_per_round.csv')
        putts_per_round_df = pd.read_csv(f'{player_data_path}/putts_per_round.csv')
        # prox_to_hole_df = pd.read_csv(f'{player_data_path}/prox_to_hole.csv')
        r1_putts_df = pd.read_csv(f'{player_data_path}/r1_putts.csv')

        # reformat data
        #prox_to_hole_df['AVG'] = prox_to_hole_df.apply(lambda x: format_prox_to_hole(x['AVG']), axis=1)

        # merge the player statistic dataframes together and format the final dataframe
        main_player_data_df = pd.merge(gir_percentage_df, total_driving_distance_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_x', '%', 'AVG']].rename(columns={'PLAYER_x': 'PLAYER_NAME', '%': 'GIR_PERCENTAGE', 'AVG': 'TOTAL_DRIVING_DISTANCE'})
        main_player_data_df = pd.merge(main_player_data_df, fir_percentage_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', '%']].rename(columns={'%': 'FIR_PERCENTAGE'})
        main_player_data_df = pd.merge(main_player_data_df, scrambling_percentage_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', '%']].rename(columns={'%': 'SCRAMBLING_PERCENTAGE'})
        main_player_data_df = pd.merge(main_player_data_df, putts_per_round_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCRAMBLING_PERCENTAGE', 'AVG']].rename(columns={'AVG': 'PUTTS_PER_ROUND'})
        main_player_data_df = pd.merge(main_player_data_df, r1_putts_df, on='PLAYER_ID', how='inner')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCRAMBLING_PERCENTAGE', 'PUTTS_PER_ROUND', 'TOTAL PUTTS']].rename(columns={'TOTAL PUTTS': 'R1_PUTTS'})


        # reorder the columns
        main_player_data_df['TOURNAMENT_NAME'] = tournament_result_csv.replace('.csv', '')
        main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'TOURNAMENT_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCRAMBLING_PERCENTAGE', 'PUTTS_PER_ROUND', 'R1_PUTTS']]

        # print and save the aggregated player data for the respective tournament
        print(f"{tournament_result_csv.replace('.csv', '')} Player Stats Dataframe:")
        print(main_player_data_df)
        print('\n')
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}")
        main_player_data_df.to_csv(f"{os.path.join(player_data_path, 'main_player_data.csv')}", index=False)

        tournament_player_data_df = pd.merge(main_player_data_df, tournament_result_df, on=['PLAYER_NAME', 'TOURNAMENT_NAME']).sort_values(by='TOTAL_SCORE', ascending=False).reset_index(drop=True)
        tournament_player_data_df = tournament_player_data_df[["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", 
            "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", 
            "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH", "R1_AVG_SCORE", "R2_AVG_SCORE", "R3_AVG_SCORE", "R4_AVG_SCORE", 
            'PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCRAMBLING_PERCENTAGE', 'PUTTS_PER_ROUND', 'R1_PUTTS',
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
    aggregate_player_and_tournament_data()
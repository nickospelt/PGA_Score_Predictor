import os
from pickle import FALSE, TRUE
import pandas as pd

main_dir = os.path.dirname(__file__)
tournament_name = "2024 Presidents Cup"

# list of all the tournament_player_data to be aggregated into final large data set
master_tournament_player_data_df = pd.DataFrame(columns=["TOURNAMENT_NAME", "ROUND_DATE", "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH", "COURSE_AVERAGE_SCORE", 'PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 
    'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', 'SCRAMBLING_PERCENTAGE', 'AVG_THREE_PUTTS_PER_ROUND', 'AVG_PUTTS_PER_ROUND', 
    "SCORE", "TOTAL_SCORE"])

# load and combine all player statistics
player_data_path = f"{main_dir}/{tournament_name}"
gir_percentage_df = pd.read_csv(f'{player_data_path}/gir_percentage.csv')
birdie_to_bogey_ratio_df = pd.read_csv(f'{player_data_path}/birdie_to_bogey_ratio.csv')
total_driving_distance_df = pd.read_csv(f'{player_data_path}/total_driving_distance.csv')
fir_percentage_df = pd.read_csv(f'{player_data_path}/fir_percentage.csv')
scoring_average_df = pd.read_csv(f'{player_data_path}/scoring_average.csv')
scrambling_percentage_df = pd.read_csv(f'{player_data_path}/scrambling_percentage.csv')
three_putts_per_round_df = pd.read_csv(f'{player_data_path}/three_putts_per_round.csv')
putts_per_round_df = pd.read_csv(f'{player_data_path}/putts_per_round.csv')

# merge the player statistic dataframes together and format the final dataframe
main_player_data_df = pd.merge(gir_percentage_df, birdie_to_bogey_ratio_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_x', '%', 'BIRDIE TO BOGEY RATIO']].rename(columns={'PLAYER_x': 'PLAYER_NAME', '%': 'GIR_PERCENTAGE', 'BIRDIE TO BOGEY RATIO': 'BIRDIE_TO_BOGEY_RATIO'})
main_player_data_df = pd.merge(main_player_data_df, total_driving_distance_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG']].rename(columns={'AVG': 'AVG_TOTAL_DRIVING_DISTANCE'})
main_player_data_df = pd.merge(main_player_data_df, fir_percentage_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', '%']].rename(columns={'%': 'FIR_PERCENTAGE'})
main_player_data_df = pd.merge(main_player_data_df, scoring_average_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'AVG']].rename(columns={'AVG': 'SCORING_AVERAGE'})
main_player_data_df = pd.merge(main_player_data_df, scrambling_percentage_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', '%']].rename(columns={'%': 'SCRAMBLING_PERCENTAGE'})
main_player_data_df = pd.merge(main_player_data_df, three_putts_per_round_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', 'SCRAMBLING_PERCENTAGE', 'AVG']].rename(columns={'AVG': 'AVG_THREE_PUTTS_PER_ROUND'})
main_player_data_df = pd.merge(main_player_data_df, putts_per_round_df, on='PLAYER_ID', how='inner')
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', 'SCRAMBLING_PERCENTAGE', 'AVG_THREE_PUTTS_PER_ROUND', 'AVG']].rename(columns={'AVG': 'AVG_PUTTS_PER_ROUND'})

# reorder the columns
main_player_data_df['TOURNAMENT_NAME'] = tournament_name
main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'TOURNAMENT_NAME', 'GIR_PERCENTAGE', 'BIRDIE_TO_BOGEY_RATIO', 'AVG_TOTAL_DRIVING_DISTANCE', 'FIR_PERCENTAGE', 'SCORING_AVERAGE', 'SCRAMBLING_PERCENTAGE', 'AVG_THREE_PUTTS_PER_ROUND', 'AVG_PUTTS_PER_ROUND']]

# print and save the aggregated player data for the respective tournament
print(f"Player Stats for {tournament_name}:")
print(main_player_data_df)
print('\n')
main_player_data_df.to_csv(f"{player_data_path}/main_player_data.csv", index=False)
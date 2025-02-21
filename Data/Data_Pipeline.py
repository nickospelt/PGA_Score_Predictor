from Tournament_Result_Scraping import scrape_tournament_results
# Merge_Tournament_Results_Player_SG_Data is the most update piece of the part of the data pipeline
from Merge_Tournament_Results_Player_Data import aggregate_player_and_tournament_data
from Merge_Tournament_Results_Player_SG_Data import aggregate_player_sg_and_tournament_data
import pandas as pd


# All relevant player Statistics must be in the correct tournament folder before running this script
scrape_tournament_results()
aggregate_player_sg_and_tournament_data()

master_dataset_df = pd.read_csv('Data/master_pga_dataset.csv')

print("Master Dataset Statistics:")
print(f"Number of Total Records: {len(master_dataset_df)}")
"""
print(f"Number of Round 1 Records: {len(master_dataset_df.loc[master_dataset_df['ROUND_NUMBER'] == 1])}")
print(f"Number of Round 2 Records: {len(master_dataset_df.loc[master_dataset_df['ROUND_NUMBER'] == 2])}")
print(f"Number of Round 3 Records: {len(master_dataset_df.loc[master_dataset_df['ROUND_NUMBER'] == 3])}")
print(f"Number of Round 4 Records: {len(master_dataset_df.loc[master_dataset_df['ROUND_NUMBER'] == 4])}")
"""
import pandas as pd

player_stat_df = pd.read_csv('Data/Player_Data/2024 The Sentry/Final_Player_Stats/gir_percentage.csv')
players_df = player_stat_df['PLAYER']
print(players_df.to_frame())

tournament_result_df = pd.read_csv('Data/Tournament_Results/2024 The Sentry.csv')
tournament_players_df = tournament_result_df['PLAYER_NAME'].rename('PLAYER')
print(tournament_players_df.to_frame())

joined = pd.merge(players_df, tournament_players_df, on='PLAYER')
print(joined)
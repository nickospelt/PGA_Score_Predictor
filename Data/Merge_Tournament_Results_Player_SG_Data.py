import os
from pickle import FALSE, TRUE
import pandas as pd

# This file works the same way as Merge_Tournament_Results_Player_Data.py but accounts for the updated SG statistics

# Convert proximity to hole averages from a string format to a numerical format
def format_prox_to_hole(value):
    feet = int(value.split("'")[0])
    inch = int(value.split("\"")[0].split(" ")[1])
    return round(feet + (inch / 12), 4)

# (1) Remove the "T" from tied positions 
# (2) Remove non-numeric characters from earnings values
def clean_tournament_results(position, earnings):
    new_position = position
    if (new_position[0] == 'T'):
        new_position = new_position[1:]
    elif (new_position[0] == '-'):
        new_position = None

    new_earnings = ""
    if (earnings != "--"):
        earnings_parts = earnings.split(",")
        if (len(earnings_parts) == 2):
            new_earnings = earnings_parts[0][1:] + earnings_parts[1]
        else:
            new_earnings = earnings_parts[0][1:] + earnings_parts[1] + earnings_parts[2]
    else:
        new_earnings = None

    return new_position, new_earnings

# ensure that player names match between both sources (espn & pga tour)
def map_player_names(player_name, name_mappings):
    new_player_name = player_name
    if new_player_name in name_mappings:
        new_player_name = name_mappings[new_player_name]
    
    return new_player_name


# Aggregate all player statistics for each individual player. Join that data with how each player played at the respective tournament
def aggregate_player_sg_and_tournament_data():
    # mappings by tournament of players with different names in pga and espn
    # espn.com (tournament_results): pgatour.com (player_data)
    # may need to flip order of keys and pairs. Creating a lot of new problems for players like Matt Fitzpatrick
    name_mappings = {
        "Sami Valimaki": "Sami Välimäki", 
        "Seamus Power": "Séamus Power",
        "Matthew Fitzpatrick": "Matt Fitzpatrick",
        "Gunnar Broin (a)": "Gunnar Broin",
        "Luke Clanton (a)": "Luke Clanton",
        "Joaquin Niemann": "Joaquín Niemann",
        "Sebastian Soderberg": "Sebastian Söderberg",
        "Blaine Hale, Jr.": "Blaine Hale Jr.",
        "Gordon Sargent (a)": "Gordon Sargent",
        "Nicolai Hojgaard": "Nicolai Højgaard",
        "Pablo Larrazabal": "Pablo Larrazábal",
        "Rasmus Hojgaard": "Rasmus Højgaard",
        "Matt NeSmith": "Matthew NeSmith",
        "Stewart Hagestad (a)": "Stewart Hagestad",
        "Travis Vick (a)": "Travis Vick",
        "Mike Lorenzo-Vera": "Michael Lorenzo-Vera",
        "Richard H. Lee": "Richard Lee",
        "Taehee Lee": "Tae Hee Lee",
        "Matt Parziale (a)": "Matt Parziale",
        "Seungsu Han": "Seung-su Han",
        "Dan Obremski": "Daniel Obremski",
        "Grady Brame": "Grady Brame Jr.",
        "Jordan Smith": "Jordan L Smith",
        "Kyung-tae Kim": "K.T. Kim"
    }

    main_dir = os.path.dirname(__file__)

    # list of all the tournament_player_data to be aggregated into final large data set
    master_tournament_player_data_df = pd.DataFrame(columns=["TOURNAMENT_NAME", "TOURNAMENT_DATE", 
        "ELEVATION", 
        "R1_TEMPERATURE", "R1_PRECIPITATION", "R1_WIND_SPEED", "R1_WIND_DIRECTION",
        "R2_TEMPERATURE", "R2_PRECIPITATION", "R2_WIND_SPEED", "R2_WIND_DIRECTION",
        "R3_TEMPERATURE", "R3_PRECIPITATION", "R3_WIND_SPEED", "R3_WIND_DIRECTION",
        "R4_TEMPERATURE", "R4_PRECIPITATION", "R4_WIND_SPEED", "R4_WIND_DIRECTION", 
        "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH",
        'PLAYER_ID', 'PLAYER_NAME', 
        'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN',
        "R1_SCORE", "R2_SCORE", "R3_SCORE", "R4_SCORE", "TOTAL_SCORE", 
        "POSITION", "EARNINGS", "FEDEX_PTS"])

    # repeat this process for each tournament result file
    for tournament_result_csv in os.listdir(os.path.join(main_dir, 'Tournament_Results')):
        # pull and clean tournament result data
        tournament_result_df = pd.read_csv(f"{os.path.join(main_dir, 'Tournament_Results')}/{tournament_result_csv}")
        tournament_result_df[['POSITION', 'EARNINGS']] = tournament_result_df.apply(lambda row: pd.Series(clean_tournament_results(row['POSITION'], row['EARNINGS'])), axis=1)
        tournament_result_df['PLAYER_NAME'] = tournament_result_df.apply(lambda row: map_player_names(row['PLAYER_NAME'], name_mappings), axis=1)

        # load and clean all player statistics (Commented out statistics not longer being used)
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}/Final Player Stats")
        
        # If a tournament doesn't have strokes gained data (British Open and Masters) then still want to get the strokes data so create empty player data frame
        # If have tee to green strokes data then have strokes gained put
        strokes_gained_f = 1
        try:
            SG_T2G_df = pd.read_csv(f'{player_data_path}/SG_T2G.csv')
        except FileNotFoundError:
            strokes_gained_f = 0
        if strokes_gained_f == 1:
            SG_PUTT_df = pd.read_csv(f'{player_data_path}/SG_PUTT.csv')

            main_player_data_df = pd.merge(SG_T2G_df, SG_PUTT_df, on='PLAYER_ID', how='inner')
            main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_x', 'TOTAL SG:PUTTING', 'SG:OTT', 'SG:APR', 'SG:ARG']].rename(columns={'PLAYER_x': 'PLAYER_NAME', 'TOTAL SG:PUTTING': 'SG_PUTT', 'SG:OTT': 'SG_OFF_THE_TEE', 'SG:APR': 'SG_APPROACH', 'SG:ARG': 'SG_AROUND_THE_GREEN'})
            main_player_data_df['SG_PUTT'] = main_player_data_df['SG_PUTT'] / 4

            main_player_data_df['TOURNAMENT_NAME'] = tournament_result_csv.replace('.csv', '')
            main_player_data_df['PLAYER_NAME'] = main_player_data_df.apply(lambda row: map_player_names(row['PLAYER_NAME'], name_mappings), axis=1)
            main_player_data_df = main_player_data_df[['PLAYER_ID', 'PLAYER_NAME', 'TOURNAMENT_NAME', 'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN']]
        else:
            player_data_columns = ['PLAYER_ID','PLAYER_NAME','TOURNAMENT_NAME','SG_PUTT','SG_OFF_THE_TEE','SG_APPROACH','SG_AROUND_THE_GREEN']
            main_player_data_df = pd.DataFrame(columns=player_data_columns)

        # print and save the aggregated player data for the respective tournament
        print(f"{tournament_result_csv.replace('.csv', '')} Player Stats Dataframe:")
        print(main_player_data_df)
        print('\n')

        # merge the player statistic dataframes together and format the final dataframe
        player_data_path = os.path.join(main_dir, f"Player_Data/{tournament_result_csv.replace('.csv', '')}")
        main_player_data_df.to_csv(f"{os.path.join(player_data_path, 'main_player_data.csv')}", index=False)
        tournament_player_data_df = pd.merge(main_player_data_df, tournament_result_df, on=['PLAYER_NAME', 'TOURNAMENT_NAME'], how='outer').sort_values(by='TOTAL_SCORE', ascending=False).reset_index(drop=True)
        tournament_player_data_df = tournament_player_data_df[["TOURNAMENT_NAME", "TOURNAMENT_DATE", 
            "ELEVATION", 
            "R1_TEMPERATURE", "R1_PRECIPITATION", "R1_WIND_SPEED", "R1_WIND_DIRECTION",
            "R2_TEMPERATURE", "R2_PRECIPITATION", "R2_WIND_SPEED", "R2_WIND_DIRECTION",
            "R3_TEMPERATURE", "R3_PRECIPITATION", "R3_WIND_SPEED", "R3_WIND_DIRECTION",
            "R4_TEMPERATURE", "R4_PRECIPITATION", "R4_WIND_SPEED", "R4_WIND_DIRECTION", 
            "COURSE_NAME", "COURSE_LOCATION", "PAR", "LENGTH",
            'PLAYER_ID', 'PLAYER_NAME', 
            'SG_PUTT', 'SG_OFF_THE_TEE', 'SG_APPROACH', 'SG_AROUND_THE_GREEN',
            "R1_SCORE", "R2_SCORE", "R3_SCORE", "R4_SCORE", "TOTAL_SCORE", 
            "POSITION", "EARNINGS", "FEDEX_PTS"]]

        print(f"{tournament_result_csv.replace('.csv', '')} Final Dataframe:")
        print(tournament_player_data_df)
        print('\n')

        # add to the master dataset
        master_tournament_player_data_df = (
            pd.concat([master_tournament_player_data_df, tournament_player_data_df])
                .sort_values(by=['TOURNAMENT_NAME', 'TOTAL_SCORE', 'PLAYER_NAME'], ascending=[False, True, True])
                .reset_index(drop=True)
        )
    print(f"Master Dataframe:")
    print(master_tournament_player_data_df)
    master_tournament_player_data_df.to_csv(f"{os.path.join(main_dir, 'master_pga_dataset.csv')}", index=False)

if __name__ == "__main__":
    aggregate_player_sg_and_tournament_data()
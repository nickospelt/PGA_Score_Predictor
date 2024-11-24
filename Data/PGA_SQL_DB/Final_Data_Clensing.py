import pandas as pd

def clean_values(value):
    clean_value = value
    if clean_value[0] == "\"":
        clean_value = clean_value[1:]
        clean_value = clean_value[:-1]

    if clean_value[len(clean_value) - 1] == "%":
        clean_value = clean_value[:-1]

    return clean_value

master_dataset_df = pd.read_csv('/Users/nickospelt/Documents/App_Projects/PGA_Score_Predictor/Data/PGA_SQL_DB/master_pga_dataset.csv')

master_dataset_df['TOURNAMENT_NAME'] = master_dataset_df['TOURNAMENT_NAME'].apply(clean_values)
master_dataset_df['COURSE_LOCATION'] = master_dataset_df['COURSE_LOCATION'].apply(clean_values)
master_dataset_df['PLAYER_NAME'] = master_dataset_df['PLAYER_NAME'].apply(clean_values)
master_dataset_df['GIR_PERCENTAGE'] = master_dataset_df['GIR_PERCENTAGE'].apply(clean_values)
master_dataset_df['FIR_PERCENTAGE'] = master_dataset_df['FIR_PERCENTAGE'].apply(clean_values)
master_dataset_df['SCRAMBLING_PERCENTAGE'] = master_dataset_df['SCRAMBLING_PERCENTAGE'].apply(clean_values)

master_dataset_df.to_csv('/Users/nickospelt/Documents/App_Projects/PGA_Score_Predictor/Data/PGA_SQL_DB/clean_master_pga_dataset.csv', index=False)



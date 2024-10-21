import pandas as pd


def convert_feet_to_number(value):
    feet = int(value.split("'")[0])
    inch = int(value.split("\"")[0].split(" ")[1])
    return round(feet + (inch / 12), 4)
    

prox_to_hole_df = pd.read_csv('/Users/nickospelt/Documents/App Projects/PGA_Score_Predictor/Data/Player_Data/2022 Fortinet Championship/Final_Player_Stats/prox_to_hole.csv')
prox_to_hole_df['AVG'] = prox_to_hole_df.apply(lambda x: convert_feet_to_number(x['AVG']), axis=1)
print(prox_to_hole_df)
print(convert_feet_to_number("40' 8\""))
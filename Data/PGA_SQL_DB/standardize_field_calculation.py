from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import sqlite3

# main function to control
if __name__ == "__main__":
    # connect to the database
    conn = sqlite3.connect('/Users/nickospelt/Documents/App_Projects/PGA_Score_Predictor/Data/PGA_SQL_DB/PGA.db')
    
    # pull historically weighted metrics
    ewa_metrics_df = pd.read_sql_query("SELECT * FROM ADJ_METRICS", conn)

    print(np.isnan(ewa_metrics_df["ADJ_SG_P"].loc[(ewa_metrics_df['PLAYER_NAME'] == "Aaron Baddeley") & (ewa_metrics_df['TOURNAMENT_NAME'] == '2017 Valspar Championship')].tolist()[0]))
    
    conn.close()
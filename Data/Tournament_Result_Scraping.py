# Packages to web scrape data
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

# Packages to save the data
import pandas as pd

# Packages to interact with Weather API
from Weather_API import get_weather_data

# Packages to convert Date correctly
from datetime import datetime

# raw_date: the dates of the tournament scraped from espn
# start_date, end_date: the start and end date of the tournament in the correct format to be passed to the weather function
def convert_dates(raw_date):
    # Break down the raw date to the individual parts
    raw_date_parts = raw_date.split(" - ")
    first_raw_date_part = raw_date_parts[0].split(" ")
    second_raw_date_part = raw_date_parts[1].split(",")
    month = first_raw_date_part[0]
    start_day = first_raw_date_part[1]
    end_day = second_raw_date_part[0]
    year = second_raw_date_part[1].strip()

    # Build both the start and end date
    start_date = month + " " + start_day + ", " + year
    end_date = month + " " + end_day + ", " + year

    # Convert start and end dates to new format
    original_format = "%B %d, %Y"
    start_date_obj = datetime.strptime(start_date, original_format)
    end_date_obj = datetime.strptime(end_date, original_format)

    new_format = "%Y-%m-%d"
    start_date = start_date_obj.strftime(new_format)
    end_date = end_date_obj.strftime(new_format)

    return start_date, end_date


# Scrapes all necessary tournament results from espn's website
def scrape_tournament_results():
    # 2023: Open - 401465539, U.S. Open - 401465533, PGA Championship - 401465523, Masters - 401465508, Players - 401465526
    # 2022: Open - 401353217, U.S. Open - 401353222, PGA Championship - 401353226, Masters - 401353232, Players - 401353254
    # 2021: Open - 401243410, U.S. Open - 401243414, PGA Championship - 401243418, Masters - 401243010, Players - 401243005
    # 2019: Open - 401056547, U.S. Open - 401056556, PGA Championship - 401056552, Masters - 401056527, Players - 401056522
    # 2018: Open - 401025259, U.S. Open - 401025255, PGA Championship - 401025263, Masters - 401025221, Players - 401025250

    tournament_ids = [401465539, 401465533, 401465523, 401465508, 401465526,
                        401353217, 401353222, 401353226, 401353232, 401353254,
                        401243410, 401243414, 401243418, 401243010, 401243005,
                        401056547, 401056556, 401056552, 401056527, 401056522,
                        401025259, 401025255, 401025263, 401025221, 401025250]

    for id in tournament_ids:
        url = f"https://www.espn.com/golf/leaderboard?tournamentId={id}"
        browser = webdriver.Chrome()
        result = browser.get(url)
        browser.implicitly_wait(5)

        web_page = browser.page_source
        soup = BeautifulSoup(web_page, "html.parser")

        # Get tournament and course information
        tournament_date = soup.find('span', class_="Leaderboard__Event__Date n7").text
        year = tournament_date.split(', ')[1]

        raw_tournament_name = soup.find('h1', class_="headline headline__h1 Leaderboard__Event__Title").text
        tournament_name = ""
        if raw_tournament_name != '2021 Masters Tournament' and raw_tournament_name != '2019 Masters Tournament' and raw_tournament_name != '2018 Masters Tournament':
            tournament_name = year + " " + soup.find('h1', class_="headline headline__h1 Leaderboard__Event__Title").text
        else:
            tournament_name = raw_tournament_name
        
        location_info = soup.find('div', class_="Leaderboard__Course__Location n8 clr-gray-04").text.split(' - ')
        course_name = location_info[0]
        course_location = location_info[1]
        course_info = soup.find('div', class_="Leaderboard__Course__Location__Detail n8 clr-gray-04").text
        par = course_info[3:5]
        length = course_info[10:]

        print(f"Scraping {tournament_name}:")

        # Get Weather Data
        start_date, end_date = convert_dates(tournament_date)
        round_date, temperature, precipitation, wind_speed, wind_direction, elevation = get_weather_data(course_location, start_date, end_date)


        r1_avg_score = 0
        r2_avg_score = 0
        r3_avg_score = 0
        r4_avg_score = 0
        
        r1_r2_player_count = 0
        r3_r4_player_count = 0

        # Get information on all players in the field
        player_rows = soup.find_all('tr', attrs={"class": "PlayerRow__Overview PlayerRow__Overview--expandable Table__TR Table__even"})
        player_count = 0
        player_results = []
        for player_row in player_rows:
            player_info = player_row.find_all('td', attrs={"class": "Table__TD"})

            player_name = player_info[2].text
            player_score = player_info[3].text
            r1_score = player_info[4].text
            r2_score = player_info[5].text
            r3_score = player_info[6].text
            r4_score = player_info[7].text
            total_score = player_info[8].text

            # Handle round information of players that played first two rounds but did not make the cut
            if player_score != 'WD' and player_score != 'MDF' and player_score != 'DQ' and r3_score == '--':
                round_1_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[0], "ROUND_NUMBER": 1, "ELEVATION": elevation, "TEMPERATURE": temperature[0], "PRECIPITATION": precipitation[0], "WIND_SPEED": wind_speed[0], "WIND_DIRECTION": wind_direction[0], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r1_score, "TOTAL_SCORE": total_score}
                round_2_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[1], "ROUND_NUMBER": 2, "ELEVATION": elevation, "TEMPERATURE": temperature[1], "PRECIPITATION": precipitation[1], "WIND_SPEED": wind_speed[1], "WIND_DIRECTION": wind_direction[1], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r2_score, "TOTAL_SCORE": total_score}
                
                r1_r2_player_count += 1
                r1_avg_score += int(r1_score)
                r2_avg_score += int(r2_score)

                player_results.append(round_1_info)
                player_results.append(round_2_info)
            # Handle round information of players that played all four rounds, or in other words made the cut
            elif player_score != 'WD' and player_score != 'MDF' and player_score != 'DQ':
                round_1_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[0], "ROUND_NUMBER": 1, "ELEVATION": elevation, "TEMPERATURE": temperature[0], "PRECIPITATION": precipitation[0], "WIND_SPEED": wind_speed[0], "WIND_DIRECTION": wind_direction[0], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r1_score, "TOTAL_SCORE": total_score}
                round_2_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[1], "ROUND_NUMBER": 2, "ELEVATION": elevation, "TEMPERATURE": temperature[1], "PRECIPITATION": precipitation[1], "WIND_SPEED": wind_speed[1], "WIND_DIRECTION": wind_direction[1], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r2_score, "TOTAL_SCORE": total_score}
                round_3_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[2], "ROUND_NUMBER": 3, "ELEVATION": elevation, "TEMPERATURE": temperature[2], "PRECIPITATION": precipitation[2], "WIND_SPEED": wind_speed[2], "WIND_DIRECTION": wind_direction[2], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r3_score, "TOTAL_SCORE": total_score}
                round_4_info = {"TOURNAMENT_NAME": tournament_name, "ROUND_DATE": round_date[3], "ROUND_NUMBER": 4, "ELEVATION": elevation, "TEMPERATURE": temperature[3], "PRECIPITATION": precipitation[3], "WIND_SPEED": wind_speed[3], "WIND_DIRECTION": wind_direction[3], "PAR": par, "LENGTH": length, "PLAYER_NAME": player_name, "SCORE": r4_score, "TOTAL_SCORE": total_score}

                r3_r4_player_count += 1
                r3_avg_score += int(r3_score)
                r4_avg_score += int(r4_score)

                player_results.append(round_1_info)
                player_results.append(round_2_info)
                player_results.append(round_3_info)
                player_results.append(round_4_info)

        # average scores for each round of the tournament
        r1_avg_score = round(r1_avg_score / r1_r2_player_count, 2)
        r2_avg_score = round(r2_avg_score / r1_r2_player_count, 2)
        r3_avg_score = round(r3_avg_score / r3_r4_player_count, 2)
        r4_avg_score = round(r4_avg_score / r3_r4_player_count, 2)

        # print(f"Tournament Name: {tournament_name}, Par: {par}, length: {length}, course rating: {course_rating}")

        # create dataframe
        tournament_information = pd.DataFrame(player_results, columns=["TOURNAMENT_NAME", "ROUND_DATE", "ROUND_NUMBER", "ELEVATION", "TEMPERATURE", "PRECIPITATION", "WIND_SPEED", "WIND_DIRECTION", "COURSE_NAME", "COURSE_LOCATION", "PLAYER_NAME", "PAR", "LENGTH", "COURSE_AVERAGE_SCORE", "SCORE", "TOTAL_SCORE"])
        tournament_information["R1_AVG_SCORE"] = r1_avg_score
        tournament_information["R2_AVG_SCORE"] = r2_avg_score
        tournament_information["R3_AVG_SCORE"] = r3_avg_score
        tournament_information["R4_AVG_SCORE"] = r4_avg_score
        tournament_information["COURSE_NAME"] = course_name
        tournament_information["COURSE_LOCATION"] = course_location

        # save dataframe
        tournament_information.to_csv(f'Data/Tournament_Results/{tournament_name}.csv', index=False)

        print(f"{tournament_name} Results Datafame:")
        print(tournament_information)
        print('\n')

        # shut down web-scraping browser
        browser.quit()

if __name__ == "__main__":
    scrape_tournament_results()
# interact with weather api
import requests

# retrieve the longitude and latitude based on a city name
from geopy.geocoders import Nominatim

import pandas as pd

# city: String in City_Name, State_Abbrev
# start_date and end_date: yyyy-mm-dd format
# Return: date, temperature, precipitation, wind_speed, wind_direction for each day between start_date, end_date inclusive
def get_weather_data(city, start_date, end_date):

    # Get longitude and latitude information
    geolocator = Nominatim(user_agent="GOLFSCOREPREDICTOR")
    location = geolocator.geocode(f"{city}")
    if location:
        city_latitude = location.latitude
        city_longitude = location.longitude
        print(f"{city} - Latitude: {city_latitude}, Longitude {city_longitude}")
    else:
        print("ERROR: Can't find Latitude and Longitude"), 

    # Retrieve Weather data
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": city_latitude,
        "longitude": city_longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
    }
    response = requests.get(url, params=params)
    weather_data = response.json()
    print(f"Weather API Results: {weather_data}")

    date = weather_data['daily']['time']
    temperature = weather_data['daily']['temperature_2m_mean']
    precipitation = weather_data['daily']['precipitation_sum']
    wind_speed = weather_data['daily']['wind_speed_10m_max']
    wind_direction = weather_data['daily']['wind_direction_10m_dominant']
    elevation = weather_data['elevation']

    return date, temperature, precipitation, wind_speed, wind_direction, elevation

def main():
    date, temperature, precipitation, wind_speed, wind_direction, elevation = get_weather_data('Kapalua, HI', '2024-08-15', '2024-08-18')

    print(f"date: {date}")
    print(f"temperature: {temperature}")
    print(f"precipitation: {precipitation}")
    print(f"wind_speed: {wind_speed}")
    print(f"wind_direction: {wind_direction}")
    print(f"elevation: {elevation}")

if __name__ == "__main__":
    main()
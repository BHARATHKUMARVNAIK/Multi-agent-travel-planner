

import requests
from crewai.tools import tool

@tool("Weather Checker")
def weather_tool(city : str) -> str:
    """
    Check the current weather and 7-day forecast for the given city.
    use this to check weather, before recommending activities.
    """

    # step - 1: get lat and long from city name 
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name" : city,
        "count" : 1,
        "language" : "en",
        "country_codes" : ["FR"]
    }
    geo_response = requests.get(geo_url, params=geo_params)    
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return f"Sorry, I couldn't find the location: {city}. Please check the city name and try again."

    # step - 2 : extract lat and long 
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    city_name = geo_data["results"][0]["name"]

    # step - 3 : get weather using lat and long
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude" : lat,
        "longitude" : lon,
        "current" : "temperature_2m,weathercode",
        "daily" : "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone" : "auto",
        "forecast_days" : 7
    }
    weather_response = requests.get(weather_url, params=weather_params)    
    weather_data = weather_response.json()

    if "current" not in weather_data:
        return f"Sorry, I couldn't retrieve weather data for {city_name}. Please try again later."

    # Step 4 — extract current temperature
    current_temp = weather_data['current']['temperature_2m']


    # Step 5 — build a readable summary string and return it
    summary = f"Current weather in {city_name}: \n"
    summary += f"Current Temperature : {current_temp}°C\n"
    summary += "7-day forecast : \n"

    days = weather_data['daily']['time']
    max_temps = weather_data['daily']['temperature_2m_max']
    min_temps = weather_data['daily']['temperature_2m_min']
    rain = weather_data['daily']['precipitation_probability_max']

    for day, max_temp, min_temp, rain_prob in zip(days, max_temps, min_temps, rain):
        summary += f"{day} - Max: {max_temp}°C, Min: {min_temp}°C, Rain Probability: {rain_prob}%\n"
    return summary





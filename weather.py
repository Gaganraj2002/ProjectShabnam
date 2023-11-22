import requests
import json


def get_weather(city, api_key):
    city = city.lower()

    # Construct the API request URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    # Send the API request and get the response
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        weather_data = json.loads(response.text)
        # Extract relevant weather information
        location = weather_data["name"]
        temperature = int(weather_data["main"]["temp"]) - 273
        description = weather_data["weather"][0]["description"]

        # Return the formatted weather information
        return f"{location} - {temperature:.2f}°C - {description}"
    else:
        return f"Error fetching weather data: {response.status_code}"


if __name__ == "__main__":
    print("Welcome to Weather App")
    city = "chennai"
    from keyFile import WEATHER_API

    # Get weather data for the specified city
    weather_info = get_weather(city, WEATHER_API)
    print(weather_info)
    # Display the weather information
    if weather_info:
        print(weather_info)
    else:
        print("Unable to retrieve weather data for", city)

    print("Have a Nice Day:)")

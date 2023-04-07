import requests
import keys


def get_weather(city):
    try:
        weather_key = keys.WEATHER_KEY
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'appid': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()

        print(weather)
        city = str(weather['name'])
        overhead = str(weather['weather'][0]['description'])
        temperature = str(get_celsius_temperature(weather['main']['temp']))
        humidity = str(weather['main']['humidity'])
        pressure = str(weather['main']['pressure'])

        chatText = "location: " + city + " " + \
                    "overhead: " + overhead + " " + \
                    "temperature: " + temperature + " " + \
                    "humidity: " + humidity + " " + \
                    "pressure: " + pressure

        text = "The weather condition of " + city + " is as follows " + "the overhead condition is " + \
               overhead + ", the temperature in Celsius is " + temperature + \
               ", pressure is " + pressure + \
               " and humidity is " + humidity
        print(">>>>>>>>" + text)
        return text, chatText
    except Exception as e:
        return "Oops! Could not find any city by this name", "Unable to fetch weather"


def get_celsius_temperature(temp):
    try:
        celsiusTemp = round(((temp-32)*5)/9, 2) 
        print(celsiusTemp)
        return celsiusTemp
    except:
        return "can't convert to celsius"
import requests
import keys
import botMessagingModule as msg

def fetchWeatherDetails():
    audio.speak("Please tell me the name of the city")
    city = audio.get_audio()
    print("city: " + str(city))
    weather_conditions = getWeatherForCity(str(city))
    audio.speak(weather_conditions)
    msg.insertMessage("Boss: " + str(weather_conditions))


def getWeatherForCity(city):
    try:
        weather_key = keys.WEATHER_KEY
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'appid': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()
        print(weather)
        text = "The weather condition of " + str(weather['name']) + " is as follows " + "the overhead condition is " + \
               str(weather['weather'][0]['description']) + ", the temperature in Celsius is " + str(get_celsius_temperature(weather['main']['temp'])) + \
               ", pressure is " + str(weather['main']['pressure']) + \
               " and humidity is " + str(weather['main']['humidity'])
        print(">>>>>>>>" + text)
        return text
    except:
        return "Oops! Could not find any city by this name"


def get_celsius_temperature(temp):
    try:
        celsiusTemp = round(((temp-32)*5)/9, 2) 
        print(celsiusTemp)
        return celsiusTemp
    except:
        return "can't convert to celsius"


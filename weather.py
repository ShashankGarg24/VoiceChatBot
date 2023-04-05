import requests
import keys
import tkinter as tk

def fetchWeatherDetails(msg):
    audio.speak("Please tell me the name of the city")
    city = audio.get_audio()
    print("city: " + str(city))
    detailedMsg, chatMsg = getWeatherForCity(str(city))
    audio.speak(detailedMsg)
    msg.insert(tk.END, "Boss: " + str(chatMsg))


def getWeatherForCity(city):
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

        chatText = "location: " + city + "\n" + \
                    "overhead: " + overhead + "\n" + \
                    "temperature: " + temperature + "\n" + \
                    "humidity: " + humidity + "\n" + \
                    "pressure: " + pressure

        text = "The weather condition of " + city + " is as follows " + "the overhead condition is " + \
               overhead + ", the temperature in Celsius is " + temperature + \
               ", pressure is " + pressure + \
               " and humidity is " + humidity
        print(">>>>>>>>" + text)
        return text, chatText
    except:
        return "Oops! Could not find any city by this name"


def get_celsius_temperature(temp):
    try:
        celsiusTemp = round(((temp-32)*5)/9, 2) 
        print(celsiusTemp)
        return celsiusTemp
    except:
        return "can't convert to celsius"


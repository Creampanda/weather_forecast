#!/usr/bin/python3
import requests
import telebot
import datetime
import config
import matplotlib.pyplot as plt
import os


def _main(city):
    owm_endpoint = "https://api.openweathermap.org/data/2.5/onecall"

    bot = telebot.TeleBot(config.token)

    if city == "Klin":
        city = config.Klin
    elif city == "Zelenograd":
        city = config.Zelenograd

    weather_params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": config.api_key,
        "exclude": "current,minutely"
    }

    will_rain = False
    counter = 0
    rain_hours = []
    weather_plot = []

    response = requests.get(owm_endpoint,params=weather_params)
    response.raise_for_status()
    weather_data = response.json()
    
    for hour in weather_data["hourly"][:23]:
        if hour["weather"][0]["id"] < 700:
            will_rain = True
            rain_hour = (datetime.datetime.now().hour + counter) % 24
            if rain_hour < 10:
                rain_hour = f"0{rain_hour}.00"
            else:
                rain_hour = f"{rain_hour}.00"
            rain_hours.append(rain_hour)
        counter += 1

    for hour in weather_data["hourly"][:23]:
        weather_plot.append(hour["temp"]-273.15)

    day_temp = round(weather_data["daily"][0]["temp"]["day"] - 273)
    night_temp = round(weather_data["daily"][0]["temp"]["night"] - 273)
    wind_speed = weather_data["daily"][0]["wind_speed"]
    sunset  = datetime.datetime.fromtimestamp(weather_data["daily"][0]["sunset"]).strftime('%H:%M')
    sunrise = datetime.datetime.fromtimestamp(weather_data["daily"][0]["sunrise"]).strftime('%H:%M')

    if will_rain:
        weather_message = f"""
            {city["name"]}
            Температура днем: {day_temp}°C
            Температура ночью: {night_temp}°C
            Cкорость ветра: до {wind_speed}м/с
            Рассвет/Закат: {sunrise}/{sunset} часов
            Ожидается дождь в {rain_hours} часов
            """
    else:
        weather_message = f"""
            {city["name"]}
            Температура днем: {day_temp}°C
            Температура ночью: {night_temp}°C
            Cкорость ветра: до {wind_speed}м/с
            Рассвет/Закат: {sunrise}/{sunset} часов
            Дождь не ожидается
            """

    x = list(range(23))
    plt.plot(x,weather_plot)
    plt.xlabel("Время")
    plt.ylabel("Градусы")
    plt.savefig("./photo/pic.png")

    bot.send_photo(config.chat_id, photo=open("./photo/pic.png","rb"), caption=weather_message )
    os.remove("./photo/pic.png")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("city",
        help="City",
        type=str)
    args = parser.parse_args()
    _main(**vars(args))

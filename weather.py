# !/Users/vadimmonroe/Desktop/Programming/_WORK_PROJECTS/16_aqara_sensors/venv/bin/python3.10

from settings import *
import requests
from telebot import TeleBot


def weather_city() -> list:
    cities_search = ["borovsk", 'miami', 'greece', 'karpathos', 'leros', 'dubai', 'los angeles',
                     'ottawa', 'canberra', 'sharm el sheikh', 'Ankara', 'sochi', 'london', 'barcelona', 'italy']
    appid = WEATHER_APP_ID
    main_list_of_cities = ['#погода_в_городах\n']

    for i in cities_search:
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': i, 'type': 'like', 'units': 'metric', 'APPID': appid})
            cities = res.json()['list'][0]

            town_help = ''
            if cities['name'] == 'Ottawa':
                town_help = f"{cities['name']} - столица Канады"
            elif cities['name'] == 'Canberra':
                town_help = f"{cities['name']} - столица Австралии"
            else:
                town_help = f"{cities['name']}"

            if cities['main']['temp'] > 0:
                temp_list = f"🌞{town_help}🌞\n°С: {cities['main']['temp']}\t\tОщущается как: {cities['main']['feels_like']}" \
                            f"\nДавление: {cities['main']['pressure']}\t\tВлажность: {cities['main']['humidity']}" \
                            f" Ветер: {cities['wind']['speed']:.0f}\nДождь: {cities['rain']}\t\tСнег: {cities['snow']}" \
                            f"\t\tОбл: {cities['clouds']['all']}\n"
            else:
                temp_list = f"❄️{town_help}❄️\n°С:️{cities['main']['temp']}️\t\tОщущается как: {cities['main']['feels_like']}" \
                            f"\nДавление: {cities['main']['pressure']}\t\tВлажность: {cities['main']['humidity']}" \
                            f" Ветер: {cities['wind']['speed']:.0f}\nДождь: {cities['rain']}\t\tСнег: {cities['snow']}" \
                            f"\t\tОбл: {cities['clouds']['all']}\n"

            # print(temp_list)
            main_list_of_cities.append(temp_list)
        except Exception as e:
            print("Exception (find):", e)
            pass

    return main_list_of_cities


def telegram_send_bot(list_of_cities: list) -> None:
    bot = TeleBot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='\n'.join(list_of_cities), parse_mode='html')


if __name__ == '__main__':
    telegram_send_bot(weather_city())

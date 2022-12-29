from aiogram import Bot, types, executor
from config import TOKEN_API, WEATHER_API
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
# from Other import number
from calc_complex import calc_complex_main
from calc_fraction import calc_fraction_main
from calc_log_reader import log_reader
import requests
import logging
# markups as nav
logging.basicConfig(level=logging.INFO)
import datetime

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!\nЯ пока что умею вычислять комплексные и вещественные числа и показывать погоду!\n"
                        "Для вывода списка комманд введите /help")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply('''Калькулятор: /calculate\nДля показа прогноза погоды введите: /weather city ''')
#
@dp.message_handler(commands=['calculate'])
async def calc_command(message: types.Message):
    await message.reply(f'''Выберите вид калькуляторов:
      Комплексные числа: /complex вид выражения при вводе -> a+bj + c-dj
      Дробные числа: /fraction вид выражения при вводе -> a/b + c/d
      Просмотр лога вычислений: /calc_log''')

@dp.message_handler(commands=['complex'])
async def complex_command(message: types.Message, command: Command):
    await message.reply(f" {calc_complex_main(command.args)}")

@dp.message_handler(commands=['fraction'])
async def fraction_command(message: types.Message, command: Command):
    await message.reply(f" {calc_fraction_main(command.args)}")

@dp.message_handler(commands=['calc_log'])
async def log_command(message: types.Message):
    await message.reply(log_reader())

@dp.message_handler(commands=['weather'])
async def choose(message: types.Message, command: Command):

    code_to_emoji = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь ☔️",
        "Drizzle": "Морось 🫧",
        "Thunderstorm": "Гроза 🌩",
        "Snow": "Снег ❄️",
        "Mist": "Туман 🌫"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={command.args}&appid={WEATHER_API}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_emoji:
            wd = code_to_emoji[weather_description]
        else:
            wd = "Посмотри в окно, не могу понять что там происходит"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        temp_max = data["main"]["temp_max"]
        temp_min = data["main"]["temp_min"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        await message.answer(f"----{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}----\n"
                            f"Прогноз погоды в местности: {city}\nС температурой воздуха: {int(cur_weather)}°C {wd}\nВлажностью воздуха: {humidity}%\nС давлением воздуха: {pressure}мм.рт.ст"
                            f"\nМаксимальная температура воздуха: {int(temp_max)}°C\nМинимальная температура воздуха: {int(temp_min)}°C\n"
                            f"Скорость ветра: {wind}м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                            f"Хорошего дня!🤗")

    except:

        await message.reply("Проверьте введенное название!")
if __name__ == '__main__':
    executor.start_polling(dp)


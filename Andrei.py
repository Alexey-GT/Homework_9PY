import requests
import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API, WEATHER_API
# import markups as nav
import random
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


# HELP_COMMAND = """
# /start - начало работы с ботом
# /help - список команд
# /Weather - Погода
# """




async def on_startup(_):
    print('Bot launched successfully!')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
        This handler will be called when user sends `/start` command
    """
    await bot.send_message(message.from_user.id, 'Приветствую тебя! {0.first_name}'.format(message.from_user) +' 👋')
    await message.delete()


# @dp.message_handler(commands=['help'])
# async def send_helper(message: types.Message):
#     """
#         This handler will be called when user sends  `/help` command
#     """
#     await message.reply(text=HELP_COMMAND)

@dp.message_handler()
async def choose(message: types.Message):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_API}&units=metric"
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
        # if message.text == '🔢 Random Number':
        #     await bot.send_message(message.from_user.id, 'Your number is: ' + str(random.randint(0, 1001)))
        # elif message.text == '🧭 Main Menu':
        #     await bot.send_message(message.from_user.id, '🧭 Main Menu', reply_markup= nav.mainMenu)
        # elif message.text == '🌤 Weather':
        #     await bot.send_message(message.from_user.id, "Погода 🌤\nМожете ввести локацию которая вас интересует 🌅")
        # elif message.text == '⏩ Other':
        #     await bot.send_message(message.from_user.id, '⏩ Other', reply_markup= nav.otherMenu)
        # elif message.text == '🤖 Info':
        #     await bot.send_message(message.from_user.id, "🧬 Fear is stupid. I'm sorry I was affraid, 1960" )
        # elif message.text == '🎵 Music':
        #     await bot.send_message(message.from_user.id, '🎵 Music', reply_markup= nav.otherMenu)
        #     await message.answer('<a href="https://music.yandex.ru">Listen to music</a>',parse_mode="HTML")
        #     await message.answer('Приятного прослушивания' + '🫶 ')
        # else:
            await message.reply("Проверьте введенное название! 🍎")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
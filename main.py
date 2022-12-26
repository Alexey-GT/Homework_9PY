from aiogram import Bot, types, executor
from config import TOKEN_API
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from calc_complex import calc_complex_main
from calc_fraction import calc_fraction_main
from calc_log_reader import log_reader


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!\nЯ пока что умею вычислять комплексные и вещественные числа!\n"
                        "Для вывода списка комманд введите /help")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply('''Калькулятор: /calculate\nЧто-нибудь еще потом: /Other ''')

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



if __name__ == '__main__':
    executor.start_polling(dp)


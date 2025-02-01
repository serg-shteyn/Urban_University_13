from aiogram import Bot,Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb.row(button1,button2)


bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())


async def mifflin(data):
	res=(int(data['growth'])*6.25)
	res+=(int(data['weight'])*10)
	res -= (int(data['age'])*5)
	res1=round(res+5,1)
	res2=round(res-161,1)
	return res1,res2

class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите ваш рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    result = await mifflin(data)
    await message.answer(f"Норма калорий в день для вас (мужчина/женщина): ({result[0]} / {result[1]})")
    await state.finish()
    
@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Нажмите "Рассчитать", чтобы посчитать необходимое количество килокалорий (ккал) в сутки для вас.',reply_markup=kb )
    
@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью')

@dp.message_handler()
async def all_messsage(message):
    await message.answer('Введите /start, чтобы посчитать необходимое количество килокалорий (ккал) в сутки для вас.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
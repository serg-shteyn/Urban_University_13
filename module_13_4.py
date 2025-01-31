# Домашнее задание по теме "Машина состояний".
# Упрощенный вариант формулы Миффлина-Сан Жеора:
#
#     для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
#     для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.

from aiogram import Bot,Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())


# Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Calories')
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
    await message.answer(f"Результат: {data}")
    await state.finish()

@dp.message_handler()
async def all_messsage(message):
    await message.answer('Введите Calories, чтобы посчитать необходимое количество килокалорий (ккал) в сутки для вас.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
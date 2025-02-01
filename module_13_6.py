# Домашнее задание по теме "Инлайн клавиатуры".

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inline.add(button1, button2)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text='Информация')
button4 = KeyboardButton(text='Рассчитать')
kb.row(button3,button4)

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


async def mifflin(data):
    try:
        res = (int(data['growth']) * 6.25)
        res += (int(data['weight']) * 10)
        res -= (int(data['age']) * 5)
        res1 = round(res + 5, 1)
        res2 = round(res - 161, 1)
        return res1, res2
    except:
        return False


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await  call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора:'
                               'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                               'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите ваш рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = await mifflin(data)
    if not result:
        await message.answer('Неправильный ввод данных')
        await state.finish()
    else:
        await message.answer(f"Норма калорий в день для вас (мужчина/женщина): ({result[0]} / {result[1]})")
        await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Формула Миффлина-Сан Жеора – это формула расчета калорий '
                         'для оптимального похудения или сохранения нормального веса.')


@dp.message_handler()
async def all_messsage(message):
    await message.answer('Введите /start для начала')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
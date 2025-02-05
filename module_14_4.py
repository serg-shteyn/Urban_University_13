# Домашнее задание по теме "План написания админ панели"

''' Дополните ранее написанный код для Telegram-бота:
Создайте файл crud_functions.py

Изменения в Telegram-бот:
В самом начале запускайте ранее написанную функцию get_all_products.
Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию get_all_products. Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
'''
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from crud_functions


kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Balance',callback_data='product_buying')
button2 = InlineKeyboardButton(text='T-Rex 3', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Forerunner 55',callback_data='product_buying')
button4 = InlineKeyboardButton(text='Watch GS 3', callback_data='product_buying')
kb_inline.add(button1, button2)
kb_inline.add(button3, button4)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button11 = KeyboardButton(text='Информация')
button22 = KeyboardButton(text='Рассчитать')
button33 = KeyboardButton(text='Купить')
kb.row(button11,button22)
kb.row(button33)

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


# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>'
@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    with open('files/Amazfit_Balance.jpg.webp','rb') as img:
    	await message.answer_photo(img,'Название: Balance | Описание: Amazfit Balance | Цена: 17000')
    with open('files/Amazfit_T-Rex_3_.webp','rb') as img:
    	await message.answer_photo(img,'Название: T-Rex 3 | Описание: Amazfit T-Rex 3 | Цена: 23000')
    with open('files/Garmin Forerunner 55_.png','rb') as img:
    	await message.answer_photo(img,'Название: Forerunner 55 | Описание: Garmin Forerunner 55 Цена: 22800')
    with open('files/HONOR_Watch_GS_3_.webp','rb') as img:
    	await message.answer_photo(img,'Название: Watch GS 3| Описание: HONOR Watch GS 3 | Цена: 12000')
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_inline)


# Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await  call.message.answer('Вы успешно приобрели продукт!')
    await  call.answer()

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await  call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора:'
                               'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                               'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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

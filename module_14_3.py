# Домашнее задание по теме "Доработка бота"

# Дополните ранее написанный код для Telegram-бота:
# Создайте и дополните клавиатуры:
#
#     В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
#     Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4". У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
#
#     Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
#     Функция get_buying_list должна выводить надписи 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза. После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное Inline меню с надписью "Выберите продукт для покупки:".
#     Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
#     Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Product1',callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3',callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_inline.add(button1, button2, button3, button4)

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


@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)

# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>'
@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    await message.answer('Название: Product1 | Описание: описание1 | Цена: <number * 100>')
    await message.answer('Название: Product2 | Описание: описание2 | Цена: <number * 100>')
    await message.answer('Название: Product3 | Описание: описание3 | Цена: <number * 100>')
    await message.answer('Название: Product4 | Описание: описание4 | Цена: <number * 100>')
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
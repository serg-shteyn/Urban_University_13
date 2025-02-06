# Домашнее задание по теме "Написание примитивной ORM"

'''
Задача "Регистрация покупателей":

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State:
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
'''

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tb_api import api
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from crud_functions import *

initiate_db()
#add_in_db()
add_user('Dmitriy','dimamen@mail.ru','41')
add_user('Sergey','shtem_x@mail.ru','44')
add_user('Vasiliy','Vasyliy77@mail.ru','47')
add_user('Maksim','maks18@mail.ru','6')

products=get_all_products()



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
button44 = KeyboardButton(text='Регистрация')
kb.row(button11,button22)
kb.row(button33)
kb.row(button44)

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

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message,state):
   await state.update_data(username=message.text)
   await message.answer('Введите свой email:')
   await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message,state):
   await state.update_data(email=message.text)
   await message.answer('Введите свой возраст:')
   await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message,state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    if is_included(data['username']):
        await message.answer('Регистрация не прошла!\nПользователь с таким именем уже есть!')
        await state.finish()
    else:
        try:
            add_user(data['username'],data['email'],data['age'])
            await message.answer('Поздравляем! Регистрация прошла успешно!')
        except:
            await message.answer('Произошла ошибка! (Не правильно введены данные)')
            await state.finish()


'''
set_username(message, state):

    Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
    Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
    Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.

set_email(message, state):

    Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
    Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
    Далее выводить сообщение "Введите свой возраст:":
    После ожидать ввода возраста в атрибут RegistrationState.age.

set_age(message, state):

    Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
    Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
    Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
    В конце завершать приём состояний при помощи метода finish().
'''

# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>'
@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    for product in products:
        with open(f'files/{product[1]}.webp','rb') as img:
            await message.answer_photo(img,f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
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
    connection.commit()
    connection.close()

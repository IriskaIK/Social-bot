from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from settings.init_tg_bot import bot, start_message, help_message, interests
from settings import keyboard as kb
from neo4jdb.db import db
import re


from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    categories = State()
    add_category = State()
    add_type = State()
    current_type = ''
    default_state = State()
    heard_type_state = State()
    heard_category_state = State()


#group
async def start(message: types.Message):
    if message.chat.type == 'private':
        if db.get_user_status(message.from_user.id) == False:
            await bot.send_message(message.from_user.id, 'текст, если юзер пишет старт боту в лс. если он еще не зареган в бд')
        else:
            await bot.send_message(message.from_user.id, 'Клавиатура с интересами. Юзер в бд', reply_markup=kb.start_kb)
    elif message.chat.type == 'group':
        if db.get_group_status(message.chat.id) == False:
            await message.answer('Инициализирую группу. Это может занять какоето время')
            db.create_group(message.chat.id, interests)
            await message.answer('Группа инициализирована. /reg чтобы зарегестрироваться.')
        else:
            await message.answer('Группа уже создана')


async def regestr_user(message: types.Message):
    if message.chat.type == 'group':
        if db.get_user_status(message.from_user.id) == False:
            db.add_user(message.from_user.id, message.chat.id, message.from_user.full_name)
            await message.reply('Вы успешно зарегестрированы')
            try:
                await bot.send_message(message.from_user.id, 'Привет!')
            except:
                await message.reply('Для продолжения работы, напишите в лс боту')
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегестрированы в другой группе.')


#private
async def help_inf(message : types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Їбать ви мишь, хелпану потім',  reply_markup=kb.start_kb)

async def view_types(message : types.Message):
    if message.chat.type == 'private':
        g_id = db.get_user_group_id(message.from_user.id)
        await Form.categories.set()
        await bot.send_message(message.from_user.id, 'Я овощ', reply_markup=kb.generate_type_keyboard(db.get_types(g_id)))
        

async def view_categories(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        Form.current_type = message.text 
        print(Form.current_type)
        await Form.add_category.set()
        g_id = db.get_user_group_id(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Я фрукт', reply_markup=kb.generate_categories_keyboard(db.get_category_by_type(g_id, message.text), message.text))

async def chose_curent_type(message : types.Message):
    if message.chat.type == 'private':
        await Form.default_state.set()
        match = re.search(r":\s(.*)", message.text)
        result = match.group(1)
        db.add_type(message.from_user.id, db.get_user_group_id(message.from_user.id), result)
        await bot.send_message(message.from_user.id, 'Успешно добавлено', reply_markup=kb.start_kb)

async def chose_category(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_category(message.from_user.id, db.get_user_group_id(message.from_user.id), message.text, Form.current_type)
        await bot.send_message(message.from_user.id, 'Успешно добавлено', reply_markup=kb.start_kb)

async def add_own_type(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await Form.heard_type_state.set()
        await bot.send_message(message.from_user.id, 'Напишите свое увлечение:')

async def add_type_to_db(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_type(message.from_user.id, db.get_user_group_id(message.from_user.id),message.text)
        await Form.default_state.set()
        await bot.send_message(message.from_user.id, 'Успешно добавлено: '+ str(message.text), reply_markup=kb.start_kb)

async def add_own_category(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await Form.heard_category_state.set()
        await bot.send_message(message.from_user.id, 'Напишите свою категорю:')

async def add_category_to_db(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_category(message.from_user.id, db.get_user_group_id(message.from_user.id), message.text, Form.current_type)
        await Form.default_state.set()
        await bot.send_message(message.from_user.id, 'Успешно добавлено: '+ str(message.text), reply_markup=kb.start_kb)

#User Navigaion

    




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state = '*')
    dp.register_message_handler(regestr_user, commands='reg', state = '*')
    dp.register_message_handler(help_inf, text='Помощь', state = '*')

    dp.register_message_handler(view_types, text='Добавить увлечение', state = '*')
    dp.register_message_handler(add_own_type, text='Добавить свое увлечение', state = '*')
    dp.register_message_handler(add_type_to_db, state=Form.heard_type_state)
    dp.register_message_handler(view_categories, state=Form.categories)


    dp.register_message_handler(add_own_category, text='Добавить свою категорию', state = '*')
    dp.register_message_handler(add_category_to_db, state=Form.heard_category_state)

    
    dp.register_message_handler(chose_curent_type, filters.Regexp('Оставить выбранное'), state = '*')
    dp.register_message_handler(chose_category, state = Form.add_category)   
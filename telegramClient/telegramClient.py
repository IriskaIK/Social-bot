from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from settings.init_tg_bot import bot, start_message, help_message, interests, BOT_TOKEN
from settings import keyboard as kb
from neo4jdb.db import db
import re
import requests


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

def something():
    db.update_value_of_relatioships('-440396677')


#group
async def start(message: types.Message):
    if message.chat.type == 'private':
        if db.get_user_status(message.from_user.id) == False:
            await bot.send_message(message.from_user.id, 'Для використання боту, створіть группу та додайте його туди, після чого напишіть /start')
        else:
            await bot.send_message(message.from_user.id, 'Привіт! Обери інтереси із запропонованих, або додай свої', reply_markup=kb.start_kb)
    elif message.chat.type == 'group':
        if db.get_group_status(message.chat.id) == False:
            await message.answer('Ініціалізую групу. Це може зайняти декілька хвилин')
            db.create_group(message.chat.id, interests)
            await message.answer('Група ініціалізована. Напишіть /reg щоб зареєструватися.')
        else:
            await message.answer('Група вже існує')


async def regestr_user(message: types.Message):
    if message.chat.type == 'group':
        if db.get_user_status(message.from_user.id) == False:
            db.add_user(message.from_user.id, message.chat.id, message.from_user.full_name, 'tg')
            await message.reply('Ви успішно зареєстровані')
            try:
                await bot.send_message(message.from_user.id, 'Привіт!', reply_markup=kb.start_kb)
            except:
                await message.reply('Для продовження роботи, напишіть боту в лс.')
        else:
            await bot.send_message(message.from_user.id, 'Ви вже зареєстровані в іншій групі.')


#private
async def help_inf(message : types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Для того, щоб почати, додайте усіх колег до групи, де є цей бот. Після цього усім треба надати інофрмацію про свої інтереси, а бот кожного дня буде надавати поради про те, кому і про що поспілкуватися',  reply_markup=kb.start_kb)

async def view_types(message : types.Message):
    if message.chat.type == 'private':
        g_id = db.get_user_group_id(message.from_user.id)
        await Form.categories.set()
        await bot.send_message(message.from_user.id, 'Виберіть серед провонованих, або додайте своє', reply_markup=kb.generate_type_keyboard(db.get_types(g_id)))
        

async def view_categories(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        Form.current_type = message.text 
        print(Form.current_type)
        await Form.add_category.set()
        g_id = db.get_user_group_id(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Виберіть серед провонованих, або додайте своє', reply_markup=kb.generate_categories_keyboard(db.get_category_by_type(g_id, message.text), message.text))

async def chose_curent_type(message : types.Message):
    if message.chat.type == 'private':
        await Form.default_state.set()
        match = re.search(r":\s(.*)", message.text)
        result = match.group(1)
        db.add_type(message.from_user.id, db.get_user_group_id(message.from_user.id), result)
        await bot.send_message(message.from_user.id, 'Успішно додано', reply_markup=kb.start_kb)

async def chose_category(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_category(message.from_user.id, db.get_user_group_id(message.from_user.id), message.text, Form.current_type)
        await bot.send_message(message.from_user.id, 'Успішно додано', reply_markup=kb.start_kb)

async def add_own_type(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await Form.heard_type_state.set()
        await bot.send_message(message.from_user.id, 'Напишіть своє захоплення:')

async def add_type_to_db(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_type(message.from_user.id, db.get_user_group_id(message.from_user.id),message.text)
        await Form.default_state.set()
        await bot.send_message(message.from_user.id, 'Успішно додано: '+ str(message.text), reply_markup=kb.start_kb)

async def add_own_category(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await Form.heard_category_state.set()
        await bot.send_message(message.from_user.id, 'Напишіть свою категорію до цього захоплення:')

async def add_category_to_db(message : types.Message, state: FSMContext):
    if message.chat.type == 'private':
        db.add_category(message.from_user.id, db.get_user_group_id(message.from_user.id), message.text, Form.current_type)
        await Form.default_state.set()
        await bot.send_message(message.from_user.id, 'Успішно додано: '+ str(message.text), reply_markup=kb.start_kb)

def send_pair(group_id, u1, u2, interests):
    user1 = db.get_username(u1)
    user2 = db.get_username(u2)
    request = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={group_id}&text=Сьогодні спілкуються @{user1} та @{user2} на їх спільні теми: {', '.join(interests)}")
    
async def create_pairs_of_user(message : types.Message, state: FSMContext):
    g_id = db.get_all_groupid()
    if bool(g_id) == True:
        for i in g_id:
            dict_of_pair, arr_of_interest, platform = db.update_value_of_relatioships(i)
            for ind, u1 in enumerate(dict_of_pair):
                if platform == 'tg':
                    send_pair(i, u1, dict_of_pair[u1], arr_of_interest[ind])

                

#User Navigaion

    




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state = '*')
    dp.register_message_handler(create_pairs_of_user, commands='create_pair', state='*')
    dp.register_message_handler(regestr_user, commands='reg', state = '*')
    dp.register_message_handler(help_inf, text='Допомога', state = '*')

    dp.register_message_handler(view_types, text='Додати захоплення', state = '*')
    dp.register_message_handler(add_own_type, text='Додати своє захоплення', state = '*')
    dp.register_message_handler(add_type_to_db, state=Form.heard_type_state)
    dp.register_message_handler(view_categories, state=Form.categories)


    dp.register_message_handler(add_own_category, text='Додати свою категорію', state = '*')
    dp.register_message_handler(add_category_to_db, state=Form.heard_category_state)

    
    dp.register_message_handler(chose_curent_type, filters.Regexp('Залишити обране'), state = '*')
    dp.register_message_handler(chose_category, state = Form.add_category)   
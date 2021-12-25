from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btnHelp = KeyboardButton('Помощь')
btnInteres = KeyboardButton('Добавить увлечение')

btnAddOwnCategory = KeyboardButton('Добавить свою категорию')
btnYourOwnHobbie = KeyboardButton('Добавить свое хобби')

def generate_type_keyboard(arr_types):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*arr_types, 'Добавить свое увлечение')
    return kb

def generate_categories_keyboard(arr_categories, parent):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('Оставить выбранное: '+str(parent),*arr_categories, 'Добавить свою категорию')
    return kb


start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnInteres, btnHelp)

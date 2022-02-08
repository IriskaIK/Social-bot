from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

btnHelp = KeyboardButton('Допомога')
btnInteres = KeyboardButton('Додати захоплення')

btnAddOwnCategory = KeyboardButton('Додати свою категорію')
btnYourOwnHobbie = KeyboardButton('Добавить свое хобби')

def generate_type_keyboard(arr_types):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*arr_types, 'Додати своє захоплення')
    return kb

def generate_categories_keyboard(arr_categories, parent):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('Залишити обране: '+str(parent),*arr_categories, 'Добавить свою категорию')
    return kb


start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnInteres, btnHelp)

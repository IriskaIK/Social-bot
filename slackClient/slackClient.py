from slack_bolt import App
from neo4jdb.db import db
from settings.init_slack_bot import interests, direct_mess_start, help_message, direct_mess_help, static_option, static_message_category, static_message_type, static_empty_message_category
from settings.slack_message_gnerator import mg
slack_bot_token = 'xoxb-2653322479682-2782803062787-TnxwvwMGCmcIWI8DEGZVQXVR'
app = App(token=slack_bot_token)

class Form():
    current_type = ''

@app.command("/start")
def start(ack ,body, say):
    ack()
    if body['channel_name'] != 'directmessage':
        if db.get_group_status(body['channel_id']) == False:
            say('Инициализирую группу. Это может занять какоето время')
            db.create_group(body['channel_id'], interests)
            say('Группа инициализирована. /reg чтобы зарегестрироваться.')
        else:
            say('Группа уже создана')
    elif body['channel_name'] == 'directmessage':
        if db.get_user_status(body['user_id']) == False:
            say('текст, если юзер пишет старт боту в лс. если он еще не зареган в бд')
        else:
            say(blocks=direct_mess_start) ##TODO: add key

@app.command("/reg")
def regestr_user(ack ,body, say):
    ack()
    user = body['user_id']
    if db.get_group_status(body['channel_id']) == True: 
        if body['channel_name'] != 'directmessage':
            if db.get_user_status(body['user_id']) == False:
                db.add_user(user, body['channel_id'], body['user_name'])
                say(f'Вы успешно зарегестрированы, <@{user}>')
                say(blocks=direct_mess_start, channel=user) ##TODO: add keyboard with interests
            else:
                say(f'Вы уже зарегестрированы в другой группе, <@{user}>')
    else:
        say(f'Сначала инициализируйте группу используя /start, <@{user}>')

@app.action("button_help")
def help_info(ack, body, say):
    ack()
    if body['channel']['name'] == 'directmessage':
        say(text=help_message)
        say(blocks=direct_mess_help)

@app.action("button_add_type")    
def view_types(ack, body, say):
    ack()
    if body['channel']['name'] == 'directmessage':
        g_id = db.get_user_group_id(body['user']['id'])
        block = mg.gen_type_block(db.get_types(g_id), static_message_type.copy(), static_option.copy(), True, 'some', static_empty_message_category)
        say(blocks=block)

@app.action("type_select")
def view_categories(ack,body, say):
    ack()
    Form.current_type = body['actions'][0]['selected_option']['text']['text']
    if body['channel']['name'] == 'directmessage':
        g_id = db.get_user_group_id(body['user']['id'])
        block = mg.gen_type_block(db.get_category_by_type(g_id, body['actions'][0]['selected_option']['text']['text']), static_message_category.copy(), static_option.copy(), False, body['actions'][0]['selected_option']['text']['text'], static_empty_message_category)
        say(blocks=block)

@app.action("choose_current_type")
def chose_curent_type(ack, body, say):
    ack()
    if body['channel']['name'] == 'directmessage':
        cur_type = body['actions'][0]['text']['text']
        db.add_type(body['user']['id'], db.get_user_group_id(body['user']['id']), cur_type)
        say(text=f'Успешно добавлено: {cur_type}')

@app.action("category_select")
def chose_category(body ,ack, say):
    ack()
    if body['channel']['name'] == 'directmessage':
        curent_category = body['actions'][0]['selected_option']['text']['text']
        db.add_category(body['user']['id'], db.get_user_group_id(body['user']['id']), curent_category, Form.current_type)
        say(text=f'Успешно добавлено: {curent_category}')

@app.action("add_own_type")
def add_new_type_to_db(ack, body, say):
    ack()
    type_one = body['actions'][0]['value']
    if body['channel']['name'] == 'directmessage':
        db.add_type(body['user']['id'], db.get_user_group_id(body['user']['id']), type_one)
        say(text=f'Успешно добавлено: {type_one}')
@app.action("add_own_category")
def add_new_category_to_db(ack, body, say):
    ack()
    category_one = body['actions'][0]['value']
    if body['channel']['name'] == 'directmessage':
        db.add_category(body['user']['id'], db.get_user_group_id(body['user']['id']), category_one, Form.current_type)
        say(text=f'Успешно добавлено: {category_one}')


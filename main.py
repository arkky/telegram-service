import logging
import json
from datetime import datetime

from sql_commands import Postgres
from misc import save_text

from aiogram import Bot, Dispatcher, executor, types

# save_text() # для сохранения текстов
# exit()

with open("tokens.json", "r") as f:
    API_TOKEN = json.load(f)['telegram']

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Set variables with texts, buttons and json
text_buttons = [
        "Parsers 🚀",
        "FAQ 🗒",
        "Profile 👔",
        "Language 🎃",
        "Terms of Use 📘",
        "Support 🆘",
        "About service 🦾",
    ]
with open("text.json", "rb") as f:
    texts = json.load(f)

language_flag = 'Russian'
language_text = {'Russian': texts['russian'], 'English': texts['english']}

users = {} # add logic to db with users UI 

#connect to db postgres
sql = Postgres()


# пример работы команды /start + добавляет кнопки, которые прожмёт пользователь и их нужно будет обработать callbacker'ом (dp.callback_query_hanlder)
# @dp.message_handler(commands='start')
# async def start_cmd_handler(message: types.Message):
#     buttons = [types.InlineKeyboardButton(f"Option: {x}", callback_data=x) for x in range(1, 4)]
#     keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
#     keyboard_markup.add(buttons[0], buttons[1], buttons[2])

#     await message.answer("Hi!\nDo you like aiogram?", reply_markup=keyboard_markup)


# пример работы встроенного меню в боте
# @dp.message_handler(commands="button")
# async def button(message: types.Message):
#     keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)

#     text_buttons = [
#         "parsers",
#         "faq",
#         "help",
#         "language",
#         "terms of use",
#         "support",
#         "profile",
#     ]

#     keyboard_markup.add(*(types.KeyboardButton(text) for text in text_buttons))

#     await message.answer("Choose option", reply_markup=keyboard_markup)


# пример ответа на любое сообщение
# @dp.message_handler()
# async def all_msg_handler(message: types.Message):
#     # pressing of a KeyboardButton is the same as sending the regular message with the same text
#     # so, to handle the responses from the keyboard, we need to use a message_handler
#     # in real bot, it's better to define message_handler(text="...") for each button
#     # but here for the simplicity only one handler is defined

#     button_text = message.text
#     logger.debug('The answer is %r', button_text)  # print the text we've got

#     if button_text == 'Yes!':
#         reply_text = "That's great"
#     elif button_text == 'No!':
#         reply_text = "Oh no! Why?"
#     else:
#         reply_text = "Keep calm...Everything is fine"

#     await message.answer(reply_text)
#     # with message, we send types.ReplyKeyboardRemove() to hide the keyboard


@dp.message_handler(commands="start")
async def start(message: types.Message):
    buttons = [types.KeyboardButton(x) for x in text_buttons]
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    keyboard_markup.add(*buttons)

    flag = sql.check_id(message.from_user.id)
    if not flag:
        sql.start_insert(message)
    
    await message.answer("Welcome!", reply_markup=keyboard_markup)


@dp.message_handler(text="Parsers 🚀")
async def parsers(message: types.Message):
    language = sql.get_language(message.from_user.id)
    text = language_text[language]['parsers']
    await message.answer(text)


@dp.message_handler(text="FAQ 🗒")
async def faq(message: types.Message):
    language = sql.get_language(message.from_user.id)
    text = language_text[language]['faq']
    await message.answer(text)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(text="Profile 👔")
async def profile(message: types.Message):
    language = sql.get_language(message.from_user.id)
    data = sql.get_profile_info(message.from_user.id)
    text = language_text[language]['profile'].format(*data, message.from_user.id)

    button = types.InlineKeyboardButton(language_text[language]['top_up_balance'], callback_data="top_up_balance")
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(button)

    await message.answer(text, reply_markup=inline_markup)


@dp.callback_query_handler(text="top_up_balance", state="*")
async def top_up_balance(query: types.CallbackQuery):
    language = sql.get_language(query.from_user.id)
    text = language_text[language]['dddd'] # введите на какую сумму в тизерах вы хотите оплатить
    
    await bot.send_message(query.from_user.id, text)
    await 


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# @dp.message_handler(text="Help")
# async def help(message: types.Message):
#     text = """
#         Если вам нужно помощь с сервисом, то свяжитесь с саппортом: @loh_pidr
#     """
#     await message.answer(text)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# block with language logic


@dp.message_handler(text="Language 🎃")
async def language(message: types.Message):
    # тут нужно добавить две кнопки инлайн, где на выбор будет Russian | English

    russian = types.InlineKeyboardButton("Russian 🇷🇺", callback_data="Russian")
    english = types.InlineKeyboardButton("English 🇺🇸", callback_data="English")

    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(russian, english)

    language = sql.get_language(message.from_user.id)

    if "Russian" == language:
        text = "На какой язык хотите поменять?"
    elif "English" == language:
        text = "What the language do you want?"
    else:
        text = "На какой язык хотите поменять?"

    await message.answer(text, reply_markup=inline_markup)


@dp.callback_query_handler(text=["Russian", "English"])
async def change_language(query: types.CallbackQuery):
    answer = query.data
    sql.change_language(query.from_user.id, language=answer)
    
    if "Russian" == answer:
        text = f"Поменяли на {answer}"
    elif "English" == answer:
        text = f"Changed to {answer}"
    else:
        text = f"Поменяли на {answer}"

    await bot.send_message(query.from_user.id, text)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(text="Terms of Use 📘")
async def terms_of_use(message: types.Message):
    language = sql.get_language(message.from_user.id)
    text = language_text[language]['terms_of_use']
    await message.answer(text)


@dp.message_handler(text="Support 🆘")
async def support(message: types.Message):
    language = sql.get_language(message.from_user.id)
    text = language_text[language]['support']
    await message.answer(text)


@dp.message_handler(text="About service 🦾")
async def about_service(message: types.Message):
    language = sql.get_language(message.from_user.id)
    text = language_text[language]['about_service']
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

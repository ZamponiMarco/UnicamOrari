import os

import telegram
from dotenv import load_dotenv
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import courses
import messages

load_dotenv()
bot_token = os.environ.get("BOT_HTTP_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    print(
        f'{update["message"]["chat"]["username"]} ({update["message"]["chat"]["first_name"]}): "{update["message"]["text"]}"')
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages.get_startup_message())



def echo(update, context):
    print(f'{update["message"]["chat"]["username"]} ({update["message"]["chat"]["first_name"]}): "{update["message"]["text"]}"')


start_handler = CommandHandler('help', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# dispatcher.add_handler(echo_handler)


years = {"0": "Tutti gli anni", "1": "Primo anno", "2": "Secondo anno", "3": "Terzo anno", "4": "Quarto anno",
         "5": "Quinto anno"}

############################### Bot ############################################


def school_start(update, context):
    update.message.reply_text(school_menu_message(),
                           reply_markup=school_menu_keyboard(), parse_mode=telegram.ParseMode.MARKDOWN)


def get_school_menu(school):
    def school_menu(update, context):
        update.callback_query.message.edit_text(course_menu_message(school),
                                             reply_markup=course_menu_keyboard(school), parse_mode=telegram.ParseMode.MARKDOWN)

    return school_menu


def get_course_menu(school, course):
    def course_menu(update, context):
        update.callback_query.message.edit_text(years_menu_message(course), reply_markup=years_menu_keyboard(school, course), parse_mode=telegram.ParseMode.MARKDOWN)
    return course_menu


def get_years_menu(school, id, course, year):
    def years_menu(update, context):
        update.callback_query.message.edit_text(get_final_message(id, course, year), reply_markup=time_menu_keyboard(school, course), parse_mode=telegram.ParseMode.MARKDOWN)
    return years_menu


############################ Keyboards #########################################


def school_menu_keyboard():
    courses_dict = courses.get_courses()
    courses_dict.keys()
    keyboard = [[InlineKeyboardButton(school, callback_data=school)] for school in courses_dict]
    return InlineKeyboardMarkup(keyboard)


def course_menu_keyboard(school):
    courses_dict = courses.get_courses()
    keyboard = [[InlineKeyboardButton(f'{single_course}', callback_data=courses_dict[school][single_course])] for single_course in
                courses_dict[school]]
    return InlineKeyboardMarkup(keyboard)


def years_menu_keyboard(school, course):
    courses_dict = courses.get_courses()
    keyboard = [[InlineKeyboardButton(f'{years[single_year]}',
                                      callback_data=f'{single_year}_{courses_dict[school][course]}')] for single_year in years]
    keyboard.append([InlineKeyboardButton(f'🔙 Torna indietro', callback_data=school)])
    return InlineKeyboardMarkup(keyboard)

def time_menu_keyboard(school, course):
    courses_dict = courses.get_courses()
    keyboard = []
    keyboard.append([InlineKeyboardButton(f'🔙 Torna indietro', callback_data=courses_dict[school][course])])
    return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################


def school_menu_message():
    return '🏫 *Seleziona la scuola*'


def course_menu_message(school):
    return f'🏫 *{school}*\n🎓 Seleziona la facoltà'

def years_menu_message(course):
    return f'🎓 *{course}*\n📅 Seleziona l\'anno'

def get_final_message(id, course, year):
    return messages.get_pretty_message(course, years[year], courses.get_timetable(id, year))

############################# Handlers #########################################


updater.dispatcher.add_handler(CommandHandler('start', school_start))
c = courses.get_courses()
for school in c:
    updater.dispatcher.add_handler(CallbackQueryHandler(get_school_menu(school), pattern=school))
    all_school_courses = c[school]
    for single_course in all_school_courses:
        updater.dispatcher.add_handler(CallbackQueryHandler(get_course_menu(school, single_course), pattern=c[school][single_course]))
        for single_year in years:
            updater.dispatcher.add_handler(CallbackQueryHandler(get_years_menu(school, c[school][single_course], single_course, single_year),
                                                                pattern=f'{single_year}_{c[school][single_course]}'))

def start_bot():
    updater.start_polling()

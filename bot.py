import os
from typing import Callable, Dict

import telegram
from dotenv import load_dotenv
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message, Chat
from telegram.ext import Updater, CallbackQueryHandler, Dispatcher
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.utils.types import CCT

import courses
import messages


def start(update, context):
    message: Message = update.message
    chat: Chat = message.chat
    print(f'{chat.username} ({chat.first_name}): "{message.text}"')
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages.get_startup_message())


def echo(update: Update, context: CCT) -> None:
    message: Message = update.message
    chat: Chat = message.chat
    print(f'{chat.username} ({message.chat["first_name"]}): "{message.text}"')


# Bot


def school_start(update: Update, context: CCT) -> None:
    update.message.reply_text(school_menu_message(),
                              reply_markup=school_menu_keyboard(), parse_mode=telegram.ParseMode.MARKDOWN)


def get_school_menu(selected_school: str) -> Callable[[Update, CCT], None]:
    def school_menu(update: Update, context: CCT) -> None:
        update.callback_query.message.edit_text(course_menu_message(selected_school),
                                                reply_markup=course_menu_keyboard(selected_school),
                                                parse_mode=telegram.ParseMode.MARKDOWN)

    return school_menu


def get_course_menu(selected_school: str, course) -> Callable[[Update, CCT], None]:
    def course_menu(update: Update, context: CCT) -> None:
        update.callback_query.message.edit_text(years_menu_message(course),
                                                reply_markup=years_menu_keyboard(selected_school, course),
                                                parse_mode=telegram.ParseMode.MARKDOWN)

    return course_menu


def get_years_menu(selected_school: str, course_id: str, course: str, year: str) -> \
        Callable[[Update, CCT], None]:
    def years_menu(update: Update, context: CCT) -> None:
        update.callback_query.message.edit_text(get_final_message(course_id, course, year),
                                                reply_markup=time_menu_keyboard(selected_school, course),
                                                parse_mode=telegram.ParseMode.MARKDOWN)

    return years_menu


# Keyboards


def school_menu_keyboard() -> InlineKeyboardMarkup:
    courses_dict = courses.get_courses()
    courses_dict.keys()
    keyboard = [[InlineKeyboardButton(selected_school, callback_data=selected_school)] for selected_school in
                courses_dict]
    return InlineKeyboardMarkup(keyboard)


def course_menu_keyboard(selected_school: str) -> InlineKeyboardMarkup:
    courses_dict = courses.get_courses()
    keyboard = [[InlineKeyboardButton(f'{selected_single_course}',
                                      callback_data=courses_dict[selected_school][selected_single_course])] for
                selected_single_course in courses_dict[selected_school]]
    return InlineKeyboardMarkup(keyboard)


def years_menu_keyboard(selected_school: str, course: str) -> InlineKeyboardMarkup:
    courses_dict = courses.get_courses()
    keyboard = [[InlineKeyboardButton(f'{years[selected_single_year]}',
                                      callback_data=f'{selected_single_year}_{courses_dict[selected_school][course]}')]
                for selected_single_year in years]
    keyboard.append([InlineKeyboardButton(f'🔙 Torna indietro', callback_data=selected_school)])
    return InlineKeyboardMarkup(keyboard)


def time_menu_keyboard(selected_school: str, course: str) -> InlineKeyboardMarkup:
    courses_dict = courses.get_courses()
    keyboard = [[InlineKeyboardButton(f'🔙 Torna indietro', callback_data=courses_dict[selected_school][course])]]
    return InlineKeyboardMarkup(keyboard)


# Messages


def school_menu_message() -> str:
    return '🏫 *Seleziona la scuola*'


def course_menu_message(selected_school: str) -> str:
    return f'🏫 *{selected_school}*\n🎓 Seleziona la facoltà'


def years_menu_message(course: str) -> str:
    return f'🎓 *{course}*\n📅 Seleziona l\'anno'


def get_final_message(course_id: str, course: str, year: str) -> str:
    return messages.get_pretty_message(course, years[year], courses.get_timetable(course_id, year))


# Handlers


load_dotenv()
bot_token: str = os.environ.get("BOT_HTTP_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater: Updater = Updater(token=bot_token, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

start_handler: CommandHandler = CommandHandler('help', start)
echo_handler: MessageHandler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

years: Dict[str, str] = {"0": "Tutti gli anni", "1": "Primo anno", "2": "Secondo anno", "3": "Terzo anno",
                         "4": "Quarto anno", "5": "Quinto anno"}

updater.dispatcher.add_handler(CommandHandler('start', school_start))
c = courses.get_courses()
for school in c:
    updater.dispatcher.add_handler(CallbackQueryHandler(get_school_menu(school), pattern=school))
    all_school_courses = c[school]
    for single_course in all_school_courses:
        updater.dispatcher.add_handler(
            CallbackQueryHandler(get_course_menu(school, single_course), pattern=c[school][single_course]))
        for single_year in years:
            updater.dispatcher.add_handler(
                CallbackQueryHandler(get_years_menu(school, c[school][single_course], single_course, single_year),
                                     pattern=f'{single_year}_{c[school][single_course]}'))


def start_bot():
    updater.start_polling()

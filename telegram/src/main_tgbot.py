#!/usr/bin/python3
import os

import telebot
from db_connector import DBConnection, FileConnection, get_time_to_update
import messages as tmsg
import server_info as sinfo
import math
import time
import datetime
from other_functions import *
import check_allowed_symbols as cas

try:
    import telegram_token
except ModuleNotFoundError:
    with open("telegram_token.py", "w", encoding="utf-8") as ttp:
        ttp.write("TOKEN = \"\"")
    import telegram_token

if telegram_token.TOKEN == "":
    token = input("Enter your Token here (or write your token in telegram_token.py file):")
else:
    token = telegram_token.TOKEN

bot = telebot.TeleBot(token)


# TODO: добавить возможность интергировать в сайт


def file_write(message, file_type, fbc):
    print(message)
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    new_file = fbc.new_file(message.audio.file_name, file_type)
    src = f"user_files/{new_file[0]}"
    with open(src, 'wb') as file:
        file.write(downloaded_file)
    bot.reply_to(message, f"{tmsg.FILE_UPLOADED}: {new_file[1]}")


# Handle all other messages.
# @bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
#     'text', 'location', 'contact', 'sticker'])

@bot.message_handler(commands=["link"])
def link(message):
    dbc = DBConnection(message.from_user.id)
    bot.send_message(message.from_user.id, f"{tmsg.YOUR_LINK}: {sinfo.ADDRESS}{dbc.get_md5()}")


@bot.message_handler(commands=["slink"])
def slink(message):
    dbc = DBConnection(message.from_user.id)
    match dbc.level():
        case 0:
            bot.send_message(message.from_user.id, tmsg.YOU_CAN_BUY_SLINK, parse_mode="MARKDOWN")
        case 1 | 2:
            link_now = dbc.get_slink()
            if link_now is not None:
                bot.send_message(message.from_user.id, f"{tmsg.YOUR_SLINK}: {sinfo.ADDRESS}{link_now}")
            else:
                bot.send_message(message.from_user.id,
                                 f"{tmsg.YOUR_SLINK_NOT_ATTACHED}\n\n{tmsg.TO_UPDATE_SLINK}", parse_mode="MARKDOWN")
            # FORBIDDEN_SLINK_SYMBOLS parse_mode="MARKDOWN"


@bot.message_handler(commands=["changeslink"])
def how_to_change_slink(message):
    dbc = DBConnection(message.from_user.id)
    if dbc.level != 0:
        bot.send_message(message.from_user.id, tmsg.TO_UPDATE_SLINK)


@bot.message_handler(commands=["switchlink"])
def switchlink(message):
    dbc = DBConnection(message.from_user.id)
    switch = dbc.switch_link()
    match switch:
        case 0:
            bot.send_message(message.from_user.id, tmsg.LINK_DEACTIVATED)
        case 1:
            bot.send_message(message.from_user.id, tmsg.LINK_ACTIVATED)


@bot.message_handler(commands=["editlink"])
def editlink(message):
    dbc = DBConnection(message.from_user.id)
    text = tmsg.EDIT
    if dbc.level() != 0:
        text += f"\n\n{tmsg.EDIT_SLINK}"
    bot.send_message(message.from_user.id, text, parse_mode="MARKDOWN")


@bot.message_handler(commands=["newlink"])
def newlink(message):
    dbc = DBConnection(message.from_user.id)
    time_to_update = dbc.new_link()
    if time_to_update == 0:
        bot.send_message(message.from_user.id, tmsg.LINK_UPDATED)
    else:
        bot.send_message(message.from_user.id, tmsg.TIME_TO_UPDATE + \
                         ": " + \
                         str(datetime.timedelta(seconds=get_time_to_update(
                             level=dbc.level(),
                             seconds=time_to_update
                         ))).split(".")[0])


@bot.message_handler(commands=["profile"])
def profile(message):
    dbc = DBConnection(message.from_user.id)
    lvl = dbc.level()
    percent = math.ceil((dbc.mb_total() / tmsg.megabytes(lvl)) * 100)
    combined_message = f"{tmsg.YOUR_PROFILE}:\n\n {tmsg.LEVEL}: {tmsg.level(lvl)}\n" + \
                       f" {tmsg.SPACE_USED}: {tmsg.disc(percent)} {math.ceil(dbc.mb_total())}" + \
                       f" из {tmsg.megabytes(lvl)} Мб\n {tmsg.ID}: {dbc.get_id()}"
    bot.send_message(message.from_user.id, combined_message, reply_markup=keyboard())


@bot.message_handler(commands=["premium"])
def premium(message):
    pass


# AUDIO
@bot.message_handler(content_types=["audio", "photo", 'voice', 'video', 'sticker'])
def handle_docs_audio(message):
    dbc = DBConnection(message.from_user.id)
    fbc = FileConnection(message.from_user.id)
    file_type = message.content_type
    msg_type = get_msg_type(file_type, message, bot)
    if msg_type == "defalut":
        return
    try:
        file_info = bot.get_file(msg_type.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        match file_type:
            case "voice":
                new_file = fbc.new_file(f"voice {time.asctime()}.ogg", file_type)
            case _:
                new_file = fbc.new_file(msg_type.file_name, file_type)
        src = f"user_files/{new_file[0]}"
        with open(src, 'wb') as file:
            file.write(downloaded_file)
        bot.reply_to(message, f"{tmsg.FILE_UPLOADED}: {new_file[1]}")
    except Exception as e:
        bot.reply_to(message, tmsg.FILE_NOT_UPLOADED)
        if dbc.level() == 2:  # only for admin
            bot.send_message(message.from_user.id, e)
        print(tmsg.LOG_ERROR, e)


# PHOTO
# @bot.message_handler(content_types=["photo"])
# def


@bot.message_handler(commands=["start"])
def start(message):
    dbc = DBConnection(message.from_user.id)
    if dbc.not_exist_telegram():
        # Новый пользователь
        dbc.new_user()
        bot.send_message(message.from_user.id, tmsg.NEW_USER, reply_markup=keyboard(), parse_mode="MARKDOWN")
    else:
        # Существующий пользователь пользователь
        bot.send_message(message.from_user.id, tmsg.EXIST_USER, reply_markup=keyboard(), parse_mode="MARKDOWN")


@bot.message_handler(commands=["help"])
def help_page(message):
    bot.send_message(message.from_user.id, tmsg.HELP, reply_markup=keyboard())


# ADMINISTRATOR FUNCTIONS
@bot.message_handler(commands=["ban"])
def ban(message):  # TODO: добавить удалённого пользователя
    dbc = DBConnection(message.from_user.id)
    command = message.text.split()

    if len(command) > 1:
        uid = command[1]
    else:
        bot.send_message(message.from_user.id, tmsg.BAN_HELP)
        return 1

    match dbc.ban(uid):
        case 0:
            bot.send_message(message.from_user.id, tmsg.NOT_BANNED)
        case 1:
            bot.send_message(message.from_user.id, tmsg.BANNED + f" {uid}")
        case 2:
            bot.send_message(message.from_user.id, tmsg.ALREADY_BANNED + f" {uid}")


@bot.message_handler(commands=["unban"])
def unban(message):
    dbc = DBConnection(message.from_user.id)
    command = message.text.split()

    if len(command) > 1:
        uid = command[1]
    else:
        bot.send_message(message.from_user.id, tmsg.BAN_HELP)
        return 1

    #    if not dbc.user_deleted(uid):
    #        bot.send_message(message.from_user.id, tmsg.USER_DELETED)
    #        return 0

    match dbc.unban(db_id=uid):
        case 0:
            bot.send_message(message.from_user.id, tmsg.NOT_BANNED)
        case 1:
            bot.send_message(message.from_user.id, tmsg.UNBANNED + f" {uid}")
        case 2:
            bot.send_message(message.from_user.id, tmsg.ALREADY_UNBANNED + f" {uid}")
    return 0


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    match message.text:
        case tmsg.PROFILE:    profile(message)
        case tmsg.GET_LINK:   link(message)
        case tmsg.SUPER_LINK: slink(message)
        case tmsg.PREMIUM:    premium(message)
        case tmsg.EDIT_LINK:  editlink(message)
    if message.text.count(":") > 0:
        command = message.text.split(":")
        dbc = DBConnection(message.from_user.id)
        sl_msg(command, message, dbc, bot, cas, sinfo)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()

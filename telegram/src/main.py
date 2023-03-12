#!/usr/bin/python3

import telebot
from db_connector import DBConnection
import messages as tmsg
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import server_info as sinfo
import time
import math

bot = telebot.TeleBot("6267477219:AAEOsa0sxy1LATKpxaBX5NmTBYPIcagViMo", parse_mode="MARKDOWN")


# TODO: добавить возможность интергировать в сайт


def keyboard():
    markup = ReplyKeyboardMarkup(row_width=2)
    row = [KeyboardButton(tmsg.PROFILE), KeyboardButton(tmsg.GET_LINK)]
    markup.add(*row)
    row = [KeyboardButton(tmsg.SUPER_LINK), KeyboardButton(tmsg.PREMIUM)]
    markup.add(*row)
    return markup


@bot.message_handler(commands=["link"])
def link(message):
    dbc = DBConnection(message.from_user.id)
    bot.send_message(message.from_user.id, f"{sinfo.ADDRESS}{dbc.get_md5()}")


@bot.message_handler(commands=["slink"])
def slink(message):
    dbc = DBConnection(message.from_user.id)
    #dbc.


@bot.message_handler(commands=["profile"])
def profile(message):
    dbc = DBConnection(message.from_user.id)
    lvl = dbc.level()
    percent = math.ceil((dbc.mb_total()/tmsg.megabytes(lvl))*100)
    combined_message = f"{tmsg.YOUR_PROFILE}:\n\n {tmsg.LEVEL}: {tmsg.level(lvl)}\n" + \
                       f" {tmsg.SPACE_USED}: {tmsg.disc(percent)} {math.ceil(dbc.mb_total())}" + \
                       f" из {tmsg.megabytes(lvl)} Мб"
    bot.send_message(message.from_user.id, combined_message)


@bot.message_handler(commands=["start"])
def start(message):
    dbc = DBConnection(message.from_user.id)
    if dbc.not_exist_telegram():
        # Новый пользователь
        dbc.new_user()
        bot.send_message(message.from_user.id, tmsg.NEW_USER)
    else:
        # Существующий пользователь пользователь
        bot.send_message(message.from_user.id, tmsg.EXIST_USER)


@bot.message_handler(commands=["help"])
def help_page(message):
    bot.send_message(message.from_user.id, tmsg.HELP, reply_markup=keyboard())


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    match message.text:
        case tmsg.PROFILE:    profile(message)
        case tmsg.GET_LINK:   link(message)
        case tmsg.SUPER_LINK: pass
        case tmsg.PREMIUM:    pass


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()

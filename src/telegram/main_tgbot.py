#!/usr/bin/python3

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


# def file_write(message, file_type, fbc):
#    print(message)
#    msg = get_msg_type(file_type)
#    file_info = bot.get_file(msg.file_id)
#    downloaded_file = bot.download_file(file_info.file_path)
#    new_file = fbc.new_file(msg.file_name, file_type)
#    src = f"user_files/{new_file[0]}"
#    with open(src, 'wb') as file:
#        file.write(downloaded_file)
#    bot.reply_to(message, f"{tmsg.FILE_UPLOADED}: {new_file[1]}")


@bot.message_handler(commands=["link"])
def link(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
    bot.send_message(message.from_user.id, f"{tmsg.YOUR_LINK}: {sinfo.ADDRESS}{dbc.get_md5()}")


@bot.message_handler(commands=["slink"])
def slink(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
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
        bot.send_message(message.from_user.id, tmsg.TO_UPDATE_SLINK, parse_mode="MARKDOWN")


@bot.message_handler(commands=["deleteslink"])
def delete_slink(message):
    dbc = DBConnection(message.from_user.id)
    if dbc.level != 0:
        if not dbc.delete_slink():
            bot.send_message(message.from_user.id, tmsg.SLINK_SUCCESSFUL_DELETED)
        else:
            bot.send_message(message.from_user.id, tmsg.SLINK_NOT_DELETED)


@bot.message_handler(commands=["switchlink"])
def switchlink(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
    switch = dbc.switch_link()
    match switch:
        case 0:
            bot.send_message(message.from_user.id, tmsg.LINK_DEACTIVATED)
        case 1:
            bot.send_message(message.from_user.id, tmsg.LINK_ACTIVATED)


@bot.message_handler(commands=["editlink"])
def editlink(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
    text = tmsg.EDIT
    if dbc.level() != 0:
        text += f"\n\n{tmsg.EDIT_SLINK}"
    bot.send_message(message.from_user.id, text, parse_mode="MARKDOWN")


@bot.message_handler(commands=["newlink"])
def newlink(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
    time_to_update = dbc.new_link()
    if time_to_update == 0:
        bot.send_message(message.from_user.id, tmsg.LINK_UPDATED)
    else:
        bot.send_message(message.from_user.id, tmsg.TIME_TO_UPDATE + ": " +
                         str(datetime.timedelta(seconds=get_time_to_update(
                             level=dbc.level(),
                             seconds=time_to_update
                         ))).split(".")[0])


@bot.message_handler(commands=["profile"])
def profile(message):
    dbc = DBConnection(message.from_user.id)
    lvl = dbc.level()
    fbc = FileConnection(message.from_user.id)
    flist = fbc.file_names_list()
    fstr = ""
    ban_word = ""
    if dbc.is_banned():
        ban_word = f" ({tmsg.BAN_WORD})"
    if len(flist) == 0:
        fmsg = ""
    else:
        for i in range(len(flist)):
            fstr += f"{i + 1}. {flist[i]}\n"
        fmsg = f"\n\n{tmsg.FILES}:\n\n{fstr}"
    percent = math.ceil((dbc.mb_total() / tmsg.megabytes(lvl)) * 100)
    combined_message = f"{tmsg.YOUR_PROFILE}:\n\n {tmsg.LEVEL}: {tmsg.level(lvl)}\n" + \
                       f" {tmsg.SPACE_USED}: {tmsg.disc(percent)} {math.ceil(dbc.mb_total())}" + \
                       f" из {tmsg.megabytes(lvl)} Мб\n {tmsg.ID}: {dbc.get_id()}{ban_word}" + fmsg
    bot.send_message(message.from_user.id, combined_message, reply_markup=keyboard())


@bot.message_handler(commands=["select"])  # TODO: Change to file help
def select(message):
    bot.send_message(message.from_user.id, tmsg.TO_SELECT_FILE, parse_mode="MARKDOWN")

# TODO: def search_file(), history(), rename_file()


@bot.message_handler(commands=["premium"])
def premium(message):
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        return
    if dbc.level() == 0:
        bot.send_message(message.from_user.id, tmsg.YOU_CAN_BUY_PREMUIM, parse_mode="MARKDOWN")
    else:
        bot.send_message(message.from_user.id, tmsg.YOU_HAVE_PREMIUM, parse_mode="MARKDOWN")


# TODO: /history for premium


# AUDIO
@bot.message_handler(content_types=["audio", "photo", "voice", "video", "sticker", "video_note"])
def handle_all_files(message):
    bot.send_message(message.from_user.id, tmsg.FLOAD_TRY)
    dbc = DBConnection(message.from_user.id)
    if banned(bot, message, dbc):
        bot.reply_to(message, tmsg.FILE_NOT_UPLOADED)
        return
    fbc = FileConnection(message.from_user.id)
    file_type = message.content_type
    msg_type = get_msg_type(file_type, message, bot)
    lvl = dbc.level()
    # using mega- 10^6 (not mebi- 2^20) bytes
    if file_type != "photo":
        fsize = msg_type.file_size / 1_000_000
    else:
        fsize = msg_type[-1].file_size / 1_000_000
    if fsize > megabytes(lvl):
        bot.send_message(message.from_user.id, tmsg.NO_SPACE)
        return
    try:
        match file_type:
            case "voice":
                new_file = fbc.new_file(f"voice_{time.asctime()}.ogg", file_type, fsize, lvl)
                file_info = bot.get_file(msg_type.file_id)
            case "audio":
                new_file = fbc.new_file(cas.file_safe_name(msg_type.file_name), file_type, fsize, lvl)
                file_info = bot.get_file(msg_type.file_id)
            case "photo":
                new_file = fbc.new_file(f"photo_{time.asctime()}.jpg", file_type, fsize, lvl)
                file_info = bot.get_file(msg_type[-1].file_id)
            case "sticker":
                file_info = bot.get_file(msg_type.file_id)
                if msg_type.is_animated:
                    new_file = fbc.new_file(f"sticker_{time.asctime()}.tgs", f"{file_type}_tgs", fsize, lvl)
                elif msg_type.is_video:
                    new_file = fbc.new_file(f"sticker_{time.asctime()}.webm", f"{file_type}_webm", fsize, lvl)
                else:
                    new_file = fbc.new_file(f"sticker_{time.asctime()}.webp", f"{file_type}_webp", fsize, lvl)
            case "video":
                new_file = fbc.new_file(f"video_{time.asctime()}.mp4", file_type, fsize, lvl)
                file_info = bot.get_file(msg_type.file_id)
            case "video_note":
                new_file = fbc.new_file(f"videonote_{time.asctime()}.mp4", file_type, fsize, lvl)
                file_info = bot.get_file(msg_type.file_id)
            case _:
                new_file = fbc.new_file(msg_type.file_name, file_type, fsize, lvl)
                file_info = bot.get_file(msg_type.file_id)

        if len(new_file) > 2:
            bot.send_message(message.from_user.id, f"{tmsg.FLOAD_DELAY} {new_file[2]} {tmsg.SECONDS}")
            return

        if new_file[0] is None:
            bot.send_message(message.from_user.id, tmsg.NO_SPACE)
            return

        new_file_name = new_file[1]

        if message.caption is not None:
            # if renamed
            if not fbc.rename_file(new_file[0], cas.file_safe_name(message.caption)):
                new_file_name = cas.file_safe_name(message.caption)

        downloaded_file = bot.download_file(file_info.file_path)
        src = f"{sinfo.PATH_TO_FILES}{new_file[0]}"
        with open(src, 'wb') as file:
            file.write(downloaded_file)
        fbc.select_file(new_file[0])
        bot.reply_to(message, f"{tmsg.FILE_UPLOADED}: {new_file_name}")

    except Exception as e:
        bot.reply_to(message, tmsg.FILE_NOT_UPLOADED)
        if dbc.level() == 2:  # only for admin
            bot.send_message(message.from_user.id, str(e))
        print(tmsg.LOG_ERROR, e)


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
def ban(message):
    dbc = DBConnection(message.from_user.id)
    command = message.text.split()

    if len(command) > 1:
        uid = command[1]
    else:
        bot.send_message(message.from_user.id, tmsg.BAN_HELP)
        return 1

    if len(command) > 2:
        reason = ""
        for i in range(len(command)-2):
            reason += command[i+2]+" "
        reason = reason[:-1]
    else:
        reason = "no reason"

    match dbc.ban(uid, reason):
        case 0:
            bot.send_message(message.from_user.id, tmsg.NOT_BANNED, parse_mode="MARKDOWN")
        case 1:
            bot.send_message(message.from_user.id, tmsg.BANNED + f" {uid}", parse_mode="MARKDOWN")
        case 2:
            bot.send_message(message.from_user.id, tmsg.ALREADY_BANNED + f" {uid}", parse_mode="MARKDOWN")
        case 4:
            bot.send_message(message.from_user.id, tmsg.INCORRECT_REASON + f" {uid}", parse_mode="MARKDOWN")


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
            bot.send_message(message.from_user.id, tmsg.NOT_BANNED, parse_mode="MARKDOWN")
        case 1:
            bot.send_message(message.from_user.id, tmsg.UNBANNED + f" {uid}", parse_mode="MARKDOWN")
        case 2:
            bot.send_message(message.from_user.id, tmsg.ALREADY_UNBANNED + f" {uid}", parse_mode="MARKDOWN")
    return 0

# TODO: add uid info command


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    match message.text:
        case tmsg.PROFILE:
            profile(message)
            return
        case tmsg.GET_LINK:
            link(message)
            return
        case tmsg.SUPER_LINK:
            slink(message)
            return
        case tmsg.PREMIUM:
            premium(message)
            return
        case tmsg.EDIT_LINK:
            editlink(message)
            return
    if message.text.count(":") > 0:
        command = message.text.split(":")
        match command[0]:
            # Change super link
            case "sl":
                dbc = DBConnection(message.from_user.id)
                if banned(bot, message, dbc):
                    return
                if dbc.level() != 0:
                    sl_msg(command, message, dbc, bot, cas, sinfo)
                else:
                    bot.send_message(message.from_user.id, tmsg.YOU_CAN_BUY_SLINK)
            # Select active file
            case "f":
                dbc = DBConnection(message.from_user.id)
                if banned(bot, message, dbc):
                    return
                fbc = FileConnection(message.from_user.id)
                flist = fbc.file_names_list()
                frawl = fbc.files_list()
                fstr = ""
                if len(flist) == 0:
                    fmsg = ""
                else:
                    for i in range(len(flist)):
                        fstr += f"{i + 1}/{frawl[i]}\n"
                try:
                    if int(command[1])-1 >= 0:
                        fbc.select_file(frawl[int(command[1])-1])
                        bot.send_message(message.from_user.id, tmsg.SELECTED_FILE + ": " +
                                         fbc.get_file_name(frawl[int(command[1])-1]))
                        return
                except IndexError:
                    bot.send_message(message.from_user.id, tmsg.FILE_NOT_FOUND)
                    return
                except ValueError:
                    bot.send_message(message.from_user.id, tmsg.ICORRECT_NUMBER)
                    return
                bot.send_message(message.from_user.id, tmsg.ICORRECT_NUMBER)
            # Delete file by number # remove_file_by_number
            case "del":
                dbc = DBConnection(message.from_user.id)
                if banned(bot, message, dbc):
                    return
                fbc = FileConnection(message.from_user.id)
                try:
                    status = fbc.remove_file_by_number(int(command[1]))
                    match status:
                        case 0:
                            bot.send_message(message.from_user.id, tmsg.FILE_DELETED)
                        case 1 | 2:
                            bot.send_message(message.from_user.id, tmsg.FILE_NOT_FOUND)
                except ValueError:
                    bot.send_message(message.from_user.id, tmsg.ICORRECT_NUMBER)
                    return

        return

    bot.send_message(message.from_user.id, tmsg.UNKNOWN_COMMAND, reply_markup=keyboard())


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()

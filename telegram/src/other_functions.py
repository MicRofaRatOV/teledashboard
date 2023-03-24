from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import messages as tmsg
from server_info import USER_MEGABYTES, PREMIUM_MEGABYTES, ADMINISTRATOR_MEGABYTES

def keyboard():
    markup = ReplyKeyboardMarkup(row_width=2)
    row = [KeyboardButton(tmsg.PROFILE), KeyboardButton(tmsg.GET_LINK), KeyboardButton(tmsg.EDIT_LINK)]
    markup.add(*row)
    row = [KeyboardButton(tmsg.SUPER_LINK), KeyboardButton(tmsg.PREMIUM)]
    markup.add(*row)
    return markup


def get_msg_type(file_type, message, bot):
    msg_type = "default"
    match file_type:
        case "audio":
            msg_type = message.audio
        case "photo":
            msg_type = message.photo
        case "voice":
            msg_type = message.voice
        case "video":
            msg_type = message.video
        case "sticker":
            msg_type = message.sticker
        case _:
            bot.send_message(message.from_user.id, tmsg.UNKNOWN_FILE_TYPE)
    return msg_type


def sl_msg(command, message, dbc, bot, cas, sinfo):
    match command[0]:
        # Update slink
        case "sl":
            match dbc.change_slink(command[1]):
                # succesful changed
                case 0:
                    bot.send_message(message.from_user.id, tmsg.SLINK_UPDATED)
                # non-changed
                case 1:
                    bot.send_message(message.from_user.id, tmsg.SLINK_OCCUPIED)
                case 2:
                    bot.send_message(message.from_user.id, tmsg.SLINK_EMPTY)
                case 3:
                    bot.send_message(message.from_user.id,
                                     tmsg.SLINK_NOT_ALLOWED_SYMBOLS + "\n\n" + tmsg.ALLOWED_SYMBOLS + ": " +
                                     cas.SLINK_SYMBOLS)
                case 4:
                    bot.send_message(message.from_user.id,
                                     tmsg.VERY_LONG_SLINK + ": " + str(sinfo.MAX_SLINK_LENGTH))

                case 5:
                    bot.send_message(message.from_user.id,
                                     tmsg.VERY_SHORT_SLINK + ": " + str(sinfo.MIN_SLINK_LENGTH))


def megabytes(lvl):
    match lvl:
        case 0:
            return USER_MEGABYTES           # user megabytes
        case 1:
            return PREMIUM_MEGABYTES        # premium megabytes
        case 2:
            return ADMINISTRATOR_MEGABYTES  # administartor megabytes

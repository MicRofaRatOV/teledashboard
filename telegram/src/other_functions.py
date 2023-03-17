from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import messages as tmsg


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
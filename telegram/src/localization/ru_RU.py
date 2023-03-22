import sys

sys.path.insert(1, '../')
import server_info as sinfo

# all_messages
PROFILE = "👤 Профиль"
GET_LINK = "🔗 Получить ссылку"
SUPER_LINK = "🌟 Суперссылка"
PREMIUM = "🌟 Премиум"
EDIT_LINK = "✏ Редактировать ссылки"
ERROR = "Ошибка"

# administrator
BANNED = "🛑 Пользователь *за*блокирован. ID"
UNBANNED = "✅ Пользователь *раз*блокирован. ID"
ALREADY_BANNED = "❗ Пользователь уже *за*блокирован. ID"
ALREADY_UNBANNED = "⚖ Пользователь уже *раз*блокирован. ID"
NOT_BANNED = "👻 Пользователя с таким id не существует"
#USER_DELETED = "☠ Пользователь с таким id удалён"
BAN_HELP = "Используй: /ban или /unban, <user id>\n\nНапрмер: /ban 1, /unban 2"

# other
LINK_UPDATED = "🔄 Ссылка упешно обновлена"
ACTIONS_TO_BUY = "вам надо написать в этот профиль: @yellow_presss"
LINK_ACTIVATED = "✅ Ваша ссылка была активирована\n\nДеактивировать - /switchlink"
LINK_DEACTIVATED = "🛑 Ваша ссылка была деактивирована\n\nАктивировать - /switchlink"
ALLOWED_SYMBOLS = "🔣 Допустимые символы"

# COMMANDS
# /start
NEW_USER = """\
Вы зарегистрированы в системе 👌

Справка по эксплуатации - /help\
"""
EXIST_USER = """\
Снова нажали на стартовую кнопку? 😁
_(хватит, пожалуйста😢)_

Справка по эксплуатации - /help\
"""

# /help
HELP = """\
📎 Справка:

     Профиль: /profile
     Получить ссылку: /link
🌟 Суперссылка: /slink
🌟 Премиум: /premium
\
"""

# /profile
YOUR_PROFILE = "📂 Ваш профиль"
SPACE_USED = "Использовано места"
LEVEL = "Уровень"
ID = "ID"


def level(lvl):
    match lvl:
        case 0:
            return "🕹 Пользователь"
        case 1:
            return PREMIUM
        case 2:
            return "👑 Администратор"


def megabytes(lvl):
    match lvl:
        case 0:
            return 15  # user megabytes
        case 1:
            return 150  # premium megabytes
        case 2:
            return 7777  # administartor megabytes


def disc(percent):
    if percent <= 30:
        return "💾"
    elif percent <= 60:
        return "💿"
    elif percent <= 80:
        return "📀"
    else:
        return "📀❗"


# /slink
YOU_CAN_BUY_SLINK = """\
🔒 У вас нет доступа к суперссылке

Суперссылка даёт вам возможность самостоятельно выбирать имя ссылки, менять её в любое время. Пример: %(link)sdefault

Чтобы получить доступ к суперссылке вам нужно получить премиум. Сделать это можно, активировав команду /premium\
""" % {'link': sinfo.ADDRESS}
YOUR_SLINK = "🌟 Ваша суперссылка"
TO_UPDATE_SLINK = "ℹ Чтобы изменить суперссылку напишите sl:*название суперссылки* (например: sl:*default*)"
SLINK_UPDATED = "🔄 Суперссылка обновлена"
FORBIDDEN_SLINK_SYMBOLS = "Вы указали недопустимые символы в суперссылке (допустиме символы: *a-Z*, *0-9*, *.*, *_*)"
YOUR_SLINK_NOT_ATTACHED = "У вас не установлена суперссылка"
SLINK_OCCUPIED = "🚫 Суперссылка занята"
SLINK_EMPTY = "🕳 Вы не ввели название суперссылки\n\nУдалить суперссылку - /deleteslink"
SLINK_NOT_ALLOWED_SYMBOLS = "⛔ Суперссылка имеет запрещённые символы"
VERY_SHORT_SLINK = "🚫 Ваша ссылка слишком короткая. Минимальная длина ссылки"
VERY_LONG_SLINK = "🚫 Ваша ссылка слишком длинная. Максмальная длина ссылки"

# /premium
YOU_CAN_BUY_PREMUIM = """\
🌟 Премиум

💸 Вы можете купить премиум прямо сейчас, для этого %(ACTIONS_TO_BUY)s\
""" % {'ACTIONS_TO_BUY': ACTIONS_TO_BUY}

# /edit
TIME_TO_UPDATE = "ℹ Вы сможете обновить ссылку через"
YOUR_LINK = "🔗 Ваша ссылка"

EDIT = """\
🔗 Действия с ссылкой:

  Получить ссылку: /link
  Обновить ссылку: /newlink
  Отключить/включить ссылку: /switchlink\
"""
EDIT_SLINK = """\
🌟 Действия с суперссылкой:

  Получить суперссылку: /slink
  Изменить суперссылку: /changeslink
  Удалить суперссылку: /deleteslink (её в любое время *можно будет восстановить*)\
"""

# FILES
FILE_UPLOADED = "Файл загружен\n\nИмя файла на сервере"
FILE_NOT_UPLOADED = "Ошибка, файл не загружен"
UNKNOWN_FILE_TYPE = "Неизвестный тип файла"

# LOG
LOG_ERROR = "[!ERROR!]"
LOG_WARNING = "(WARNING)"
LOG_INFO = "[INFO]"

# import sys
import datetime
from other_functions import megabytes
import server_info as sinfo

# all_messages
PROFILE = "👤 Профиль"
GET_LINK = "🔗 Получить ссылку"
SUPER_LINK = "🌟 Суперссылка"
PREMIUM = "🌟 Премиум"
EDIT_LINK = "✏ Редактировать ссылки"
LOAD_FILE = "📂 Управление файлами"
ERROR = "Ошибка"
UNKNOWN_COMMAND = "❓ Неизвестная команда"

# administrator
BANNED = "🛑 Пользователь *за*блокирован. ID"
UNBANNED = "✅ Пользователь *раз*блокирован. ID"
ALREADY_BANNED = "❗ Пользователь уже *за*блокирован. ID"
ALREADY_UNBANNED = "⚖ Пользователь уже *раз*блокирован. ID"
NOT_BANNED = "👻 Пользователя с таким id не существует"
# USER_DELETED = "☠ Пользователь с таким id удалён"
BAN_HELP = "Используй: /ban или /unban, <user id>\n\nНапрмер: /ban 1, /unban 2"

# ban
YOU_ARE_BANNED = """❗ Вы не можете воспользоваться данной комндой, вы заблокированы

По вопросам разблокировки: @yellow_presss"""
BAN_WORD = "заблокирован"
INCORRECT_REASON = "❌ Неверная причина"

# other
LINK_UPDATED = "🔄 Ссылка упешно обновлена"
ACTIONS_TO_BUY = ", для этого вам надо написать: @yellow\_presss"
LINK_ACTIVATED = "✅ Ваша ссылка была активирована\n\nДеактивировать - /switchlink"
LINK_DEACTIVATED = "🛑 Ваша ссылка была деактивирована\n\nАктивировать - /switchlink"
ALLOWED_SYMBOLS = "🔣 Допустимые символы"
ICORRECT_NUMBER = "🛑 Введена некорректная величина"
SECONDS = "сек"

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
YOUR_PROFILE = "📊 Ваш профиль"
SPACE_USED = "Использовано места"
LEVEL = "Уровень"
ID = "ID"
FILES = "📂 Ваши файлы (/file)"
TO_SELECT_FILE = "ℹ Чтобы выбрать отображаемый напишите F:*номер файла* (например: `F:1`)"
TO_DELETE_FILE = "🛑 Чтобы удалить файл DEL:*номер файла* (или `DEL:all`, чтобы удалить все файлы)"


def level(lvl):
    match lvl:
        case 0:
            return "🕹 Пользователь"
        case 1:
            return PREMIUM
        case 2:
            return "👑 Администратор"


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
TO_UPDATE_SLINK = "ℹ Чтобы изменить суперссылку напишите SL:*название суперссылки* (например: `SL:default`)"
SLINK_UPDATED = "🔄 Суперссылка обновлена"
FORBIDDEN_SLINK_SYMBOLS = "Вы указали недопустимые символы в суперссылке (допустиме символы: *a-Z*, *0-9*, *.*, *_*)"
YOUR_SLINK_NOT_ATTACHED = "У вас не установлена суперссылка"
SLINK_OCCUPIED = "🚫 Суперссылка занята"
SLINK_EMPTY = "🕳 Вы не ввели название суперссылки\n\nУдалить суперссылку - /deleteslink"
SLINK_NOT_ALLOWED_SYMBOLS = "⛔ Суперссылка имеет запрещённые символы"
VERY_SHORT_SLINK = "🚫 Ваша ссылка слишком короткая. Минимальная длина ссылки"
VERY_LONG_SLINK = "🚫 Ваша ссылка слишком длинная. Максмальная длина ссылки"
SLINK_SUCCESSFUL_DELETED = "🗑 Суперссылка успешно удалена"
SLINK_NOT_DELETED = "⛔ Суперссылка не удалена (возможно она уже удалена/ещё не задана)"

# /premium
YOU_CAN_BUY_PREMUIM = f"""\
🌟 У вас нет премиума

🌟 Что даёт премиум?

· 🕛 *Загрузка* файлов раз в *{sinfo.PREMIUM_LTIME} сек*, вместо {sinfo.USER_LTIME}
· 📀 *{megabytes(1)} мб* загруженных файлов вместо {megabytes(0)}
· 📁 *{sinfo.PREMIUM_FILE_COUNT}* файлов на сервере вместо {sinfo.USER_FILE_COUNT}
· 🔑 Доступ к суперссылке /slink
· 🔗 Смена обычной ссылки раз в \
{str(datetime.timedelta(seconds=sinfo.PREMIUM_CHANGE_TIME * 86400)).split(".")[0]}, вместо \
{str(datetime.timedelta(seconds=sinfo.DEFAULT_CHANGE_TIME * 86400)).split(".")[0]}

💸 Вы можете купить премиум прямо сейчас%(ACTIONS_TO_BUY)s\
""" % {'ACTIONS_TO_BUY': ACTIONS_TO_BUY}

YOU_HAVE_PREMIUM = f"""\
🌟 *Премиум*

🌟 Премиум команды:

· *Суперссылка* /slink

🌟 Премиум преимущества:

· 🕛 *Загрузка* файлов раз в *{sinfo.PREMIUM_LTIME} сек*, вместо {sinfo.USER_LTIME}
· 📀 *Обновление* ссылки раз в \
*{str(datetime.timedelta(seconds=sinfo.PREMIUM_CHANGE_TIME * 86400)).split(".")[0]}*, вместо \
{str(datetime.timedelta(seconds=sinfo.DEFAULT_CHANGE_TIME * 86400)).split(".")[0]}
· 🔑 *Бесконечное* обновление суперссылки
· 📀 *{megabytes(1)} мб* загруженных файлов вместо {megabytes(0)} мб
· 📁 *{sinfo.PREMIUM_FILE_COUNT}* файлов на сервере
\
"""

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
  Изменить/Установить суперссылку: /changeslink
  Удалить суперссылку: /deleteslink (её в любое время *можно будет установить*)\
"""

# FILES
FILE_UPLOADED = "📥 Файл загружен\n\nИмя файла на сервере"
FILE_NOT_UPLOADED = "🔌 Ошибка, файл не загружен"
UNKNOWN_FILE_TYPE = "Неизвестный тип файла"
FLOAD_TRY = "⌛ Попытка загрузить файл"
FLOAD_DELAY = "⏳ Вы пока не можете загрузить файл, подождите"
NO_SPACE = "💽 У вас не хватат места на облачном диске!"
SELECTED_FILE = "💾 Выбран файл"
FILE_NOT_FOUND = "📭 Файл не найден"
FILE_DELETED = "🕳️ Файл удалён"

# LOG
LOG_ERROR = "[!ERROR!]"
LOG_WARNING = "(WARNING)"
LOG_INFO = "[INFO]"

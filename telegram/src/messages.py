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


def level(lvl):
    match lvl:
        case 0: return "🕹 Пользователь"
        case 1: return PREMIUM
        case 2: return "👑 Администратор"


def megabytes(lvl):
    match lvl:
        case 0: return 15    # user megabytes
        case 1: return 150   # premium megabytes
        case 2: return 7777  # administartor megabytes


def disc(percent):
    if percent <= 30:
        return "💾"
    elif percent <= 60:
        return "💿"
    elif percent <= 80:
        return "📀"
    else:
        return "📀❗"



# all_messages
PROFILE = "👤 Профиль"
GET_LINK = "🔗 Получить ссылку"
SUPER_LINK = "🌟 Суперссылка"
PREMIUM = "🌟 Премиум"


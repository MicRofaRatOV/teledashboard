# Links https
ADDRESS = "https://example.com/"  # dont forget slash!!!

# DB Links
DBL = "../db/user.db"  # DONT FORGET to change after built to ABSOLUTE PATH

# Files
MAX_EPONYMOUS_FILES = 9  # maximum number of files with the same name per user
PATH_TO_FILES = "../php_root/user_files/"
PATH_TO_DELETED = "../.deleted/"
MAX_FILE_NAME_LENGTH = 64  # dont use values higher than 128 (you can take very long message and telegram error)

# Megabytes
USER_MEGABYTES = 15
PREMIUM_MEGABYTES = 150
ADMINISTRATOR_MEGABYTES = 7777

# Load time (sec)
USER_LTIME = 15
PREMIUM_LTIME = 5
ADMINISTRATOR_LTIME = 0

# Max file count (dont use values higher than 32)
USER_FILE_COUNT = 10
PREMIUM_FILE_COUNT = 20
ADMINISTRATOR_FILE_COUNT = 32

# Link (days)
DEFAULT_CHANGE_TIME = 14
PREMIUM_CHANGE_TIME = 0.0208

# Super link
MAX_SLINK_LENGTH = 32
MIN_SLINK_LENGTH = 4  # not recommended <= 2

# Symbols
SLINK_SYMBOLS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789_"  # Dont use "." symbol
FILE_SYMBOLS = """qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789_.,%#@!№;&()+-=~\
йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"""

# Roots
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

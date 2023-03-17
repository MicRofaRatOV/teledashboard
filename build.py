import os
import shutil
from distutils.dir_util import copy_tree

try:
    os.mkdir("project")
except FileExistsError:
    if input("! Folder \"project\" will be cleared. Continue? [N/y]").lower() == "y":
        shutil.rmtree("./project")
        os.mkdir("project")
        print()
    else:
        exit(0)

# vars
telegram_root = "telegram/src/"
database_root = "telegram/src/db/"

# lists
telegram_files = [
    "main_tgbot.py",
    "db_connector.py",
    "random_generator.py",
    "messages.py",
    "server_info.py"
]


def main():
    # Telegram
    print("Making telegram folder")
    os.mkdir("project/telegram")
    print("  Copying telegram/src python files")
    for file in telegram_files:
        shutil.copy(telegram_root+file, "project/telegram/")
    print("  Done\n")

    # Telegram localization
    print("Making telegram localization folder")
    os.mkdir("project/telegram/localization")
    print("  Copying telegram/src/localization folder")
    copy_tree("telegram/src/localization", "project/telegram/localization")
    print("  Done\n")

    # Telegram user_files
    print("Making telegram user_files folder")
    os.mkdir("project/telegram/user_files")
    os.mkdir("project/telegram/user_files/.deleted")
    print("  Done\n")

    # Databse
    print("Making database folder")
    os.mkdir("project/database")
    print("  Copying emtpy.db to user.db")
    shutil.copy(database_root+"empty.db", "project/database/user.db")
    print("  Done\n")


    print("""\
[TIP]: Dont forget to configure:
  project/telegram/server_info.py
  project/telegram/messages.py       [optional]
  project/telegram/telegram_token.py [optional]\
""")


if __name__ == "__main__":
    main()
#!/usr/bin/python3

import time
import sqlite3

# Settings
DB_FOLDER = "./db/"
UPDATE_TIME = 60*5  # seconds


def main():
    while True:
        con_usr = sqlite3.connect(DB_FOLDER+"user.db")
        cur_usr = con_usr.cursor()

        con_web = sqlite3.connect(DB_FOLDER+"web.db")
        cur_web = con_web.cursor()

        try:
            file_count = cur_usr.execute("SELECT COUNT() FROM file").fetchone()[0]
            user_count = cur_usr.execute("SELECT COUNT() FROM user").fetchone()[0]

            cur_web.execute(f"INSERT or IGNORE INTO stat VALUES ({int(time.time())}, {user_count}, {file_count})")
            con_web.commit()
        except Exception as e:
            print(e)
        finally:
            con_usr.close()
            con_web.close()

        time.sleep(UPDATE_TIME)


if __name__ == "__main__":
    main()

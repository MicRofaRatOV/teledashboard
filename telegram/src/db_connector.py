import sqlite3
import time
import random_generator as rgen
import math
import server_info as sinfo
import shutil
import os
import messages as tmsg


# id - local id
# link - md5 уникальный hash для ссылки
# level - уровень аккаунта (
#   0: базовый
#   1: премиум
#   2: администратор
# )
# reg_time - timestamp регистрации
# mb_total - количество мегабайт занято (байт*10^6)
# telegram - telegram id
# super_link - рукописная ссылка
# ban - уровень аккаунта (
#   0: нет блокировок
#   1: забанен
#   -1: аккаунт удалён пользователем
# )
# title - заголовок страницы в браузере
# mb_traffic - количество мегабайт принято за всё время (байт*10^6)

def itime():
    return int(time.time())


# DBLink
DB = sinfo.DBL


class Connection:
    def __init__(self, telegram_id=0, path=DB):
        self._db_link = path  # Path to database
        self._tg_id = str(telegram_id)
        self._con = sqlite3.connect(self._db_link)
        self._cur = self._con.cursor()

    def __del__(self):
        self._con.close()

    def connection(self):
        return self._con

    def exec(self, command):
        return self._cur.execute(command)

    # TODO: add not exist protection
    def select(self, table, result_column, expr):
        return self.exec(
            """ SELECT (%(result_column)s)
            FROM %(table)s WHERE (%(expr)s)"""
            % {'result_column': result_column,
               'table': table, 'expr': expr}
        )

    def insert(self, table, column_name, values):
        self.exec(
            """ INSERT OR IGNORE INTO %(table)s
            (%(column_name)s) VALUES (%(values)s)"""
            % {'table': table, 'column_name': column_name,
               'values': values}
        )
        self._con.commit()

    def update(self, table, column_name, values, condition):
        self.exec(
            """ UPDATE OR IGNORE %(table)s SET
            (%(column_name)s) = (%(values)s)
            WHERE %(condition)s"""
            % {'table': table, 'column_name': column_name,
               'values': values, 'condition': condition}
        )
        self._con.commit()

    def not_exist_telegram(self, tg_id=-1):
        if tg_id == -1: tg_id = self._tg_id
        if not self.select("user", "telegram", f"telegram={tg_id}").fetchall():
            return True
        else:
            return False

    def not_exist_id(self, uid):
        if not self.select("user", "id", f"id={uid}").fetchall():
            return True
        else:
            return False

    def get_id(self):
        return self.select("user", "id", f"telegram={self._tg_id}").fetchall()[0][0]


def level_time(lvl):
    match lvl:
        case 0:
            return 14  # default user
        case 1:
            return 0.0208  # premium user
        case 2:
            return 0  # administrator
        case _:
            return 0  # other


def get_time_to_update(level, seconds):
    days = level_time(level)
    return (86400 * days) - seconds


class DBConnection(Connection):
    def __init__(self, telegram_id=0, path=DB):
        self._db_link = path  # Path to database
        self._tg_id = str(telegram_id)
        self._con = sqlite3.connect(self._db_link)
        self._cur = self._con.cursor()
        if self.not_exist_telegram():
            self._md5_link = rgen.generate_md5_str()
        else:
            self._md5_link = self.get_md5()

    # def info(self):
    #    return f"db_link={self._db_link}\n_tg_id={self._tg_id}"

    #    def change_id_to(self, telegram_id=0):
    #        self._tg_id = telegram_id

    def get_md5(self):
        if self.not_exist_telegram():
            self.new_user()
            return self.get_md5()
        else:
            return self.select(table="user",
                               result_column="link",
                               expr=f"telegram={self._tg_id}").fetchall()[0][0]

    # Dont touch this function

    def not_exist_id(self, uid):
        if not self.select("user", "id", f"id={uid}").fetchall():
            return True
        else:
            return False

    def switch_link(self):
        old_condition = self.select("user", "activate_link", f"telegram={self._tg_id}").fetchall()[0][0]
        match old_condition:
            case 0:
                self.update("user", "activate_link", "1", f"telegram={self._tg_id}")
                return 1  # link activated
            case 1:
                self.update("user", "activate_link", "0", f"telegram={self._tg_id}")
                return 0  # link deactivated

    def add_link_to_log(self):
        if not self.select("user", "link_log", f"telegram={self._tg_id}").fetchall()[0][0]:
            # Empty link log
            self.update("user", "link_log", f"'{self._md5_link}'", f"telegram={self._tg_id}")
            return True  # code 1
        else:
            old_link_log = self.select("user", "link_log", f"telegram={self._tg_id}").fetchall()[0][0]
            if old_link_log.split("|")[-1] == self._md5_link:
                return True  # code 1
            else:
                self.update("user", "link_log", f"'{old_link_log}|{self._md5_link}'", f"telegram={self._tg_id}")
                return False  # code 0

    def level(self):
        if self.not_exist_telegram():
            self.new_user()
            return 0  # Пользователь
        else:
            self.add_link_to_log()
            match int(self.select(table="user", result_column="level",
                                  expr=f"telegram={self._tg_id}").fetchall()[0][0]):
                case 0:
                    return 0  # Пользователь
                case 1:
                    return 1  # Премиум
                case 2:
                    return 2  # Админимтратор
            # else (_ / default):
            self.update("user", "level", "0", f"telegram={self._tg_id}")
            return self.level()

    def mb_total(self):
        return self.select("user", "mb_total", f"telegram={self._tg_id}").fetchall()[0][0]

    def get_slink(self):
        if self.not_exist_telegram():
            return None
        return self.select("user", "super_link", f"telegram={self._tg_id}").fetchall()[0][0]


    def new_link(self):
        lvl = self.level()
        days = level_time(lvl)
        link_time = int(self.select("user", "link_time", f"telegram='{self._tg_id}'").fetchall()[0][0])
        if math.ceil(itime() - link_time) > 86400 * days:
            self._md5_link = rgen.generate_md5_str()
            self.update("user", "link, link_time", f"'{self._md5_link}', {itime()}", f"telegram={self._tg_id}")
            return 0
        else:
            return math.ceil(itime() - link_time)

    def new_user(self):
        self.insert(table="user",
                    column_name="""link, level, reg_time, mb_total, telegram, ban, title, mb_traffic,
                                   activate_link, link_time, click, link_log""",
                    values=f"""'{self._md5_link}', 0, {itime()}, 0.0, {self._tg_id}, 0, 'My Page', 0.0, 
                               0, {itime()}, 0, '{self._md5_link}'""")

    # ADMINISTARATOR FUNCTIONS
    def ban(self, db_id):  # TODO: добавить удалённого пользователя
        if self.not_exist_id(db_id):
            return 0  # user not exist
        if self.select("user", "ban", f"id={db_id}").fetchall()[0][0] == 1:
            return 2  # already banned
        self.update("user", "ban", "1", f"id={db_id}")
        return 1  # user is successfully BANNED

    def unban(self, db_id):
        if self.not_exist_id(db_id):
            return 0  # user not exist
        if self.select("user", "ban", f"id={db_id}").fetchall()[0][0] == 0:
            return 2  # already unbanned
        self.update("user", "ban", "0", f"id={db_id}")
        return 1  # user is successfully unbanned

    #def user_deleted(self, uid):
    #    return self.select("user", "")

# FILE BD CONNECTION
# key - md5 name of file
# owner - user_id
# status
#    0 active
#    1 moved to trash (.deleted)
#   -1 removed from drive
# name - original name of file
# load_time - timestamp of load
# deletion_time - timestamp of delete / -1 - file isnt deleted


class FileConnection(Connection):
    def __init__(self, telegram_id=0, path=DB):
        self._db_link = path  # Path to database
        self._tg_id = str(telegram_id)
        self._con = sqlite3.connect(self._db_link)
        self._cur = self._con.cursor()
        if not self.not_exist_telegram(int(self._tg_id)):
            self._uid = self.get_id()
        else:
            self._uid = 0

    def get_path_to_file(self, file_name):
        if self.is_user_exist() and self.is_file_exist(file_name):
            return self.select("file", "key", f"name='{file_name}' AND owner={self._uid}").fetchall()[0][0]
        else:
            return []

    def is_user_exist(self):
        if self._uid == 0:
            return False
        else:
            return True

    def is_file_exist(self, file_name, owner=0):
        if owner == 0: owner = self._uid
        if self.select("file", "key", f"name='{file_name}' AND owner={owner}").fetchall():
            return True
        else:
            return False

    def is_key_exist(self, key):
        if self.select("file", "key", f"key='{key}'").fetchall():
            return True
        else:
            return False

    # For deleted and non-deleted files
    def get_file_key_anyway(self, file_name, owner):
        if self.is_file_exist(file_name):
            return self.select("file", "key", f"name='{file_name}' AND owner={owner}").fetchall()[0][0]
        else:
            return "default"

    def get_file_key(self, file_name, owner=0):
        if owner == 0: owner = self._uid
        key = self.get_file_key_anyway(file_name, owner)
        if not self.is_file_killed(key):
            return key
        else:
            return None

    def is_file_deleted(self, key):
        if not self.is_key_exist(key):
            return True
        if self.select("file", "status", f"key='{key}'").fetchall()[0][0] == 0:
            return False
        else:
            return True

    def is_file_killed(self, key):
        if not self.is_key_exist(key):
            return True
        if self.select("file", "status", f"key='{key}'").fetchall()[0][0] == -1:
            return True
        else:
            return False

    def files_list(self):
        list_of_files = []
        for x in self.select("file", "key", f"owner={self._uid} AND status=0").fetchall():
            list_of_files.append(x[0])
        return list_of_files

    def get_file_name(self, key):
        if self.is_key_exist(key):
            return self.select("file", "name", f"key='{key}'").fetchall()[0][0]

    def full_files_list(self):
        pass

    def get_file_type(self, key="default", name="default"):
        if key == "defalut": key = self.get_file_key(name)
        if self.is_key_exist(key):
            return self.select("file", "file_type", f"key='{key}'").fetchall()[0][0]

    def new_file(self, file_name, file_type):
        key = rgen.generate_md5_str()
        if not self.get_path_to_file(file_name):
            # if user dont have two or comre files with same names
            # yeas, my English B)
            self.insert(
                table="file",
                column_name="key, owner, status, name, load_time, deletion_time, file_type",
                values=f"'{key}', {self._uid}, 0, '{file_name}', {itime()}, -1, '{file_type}'"
            )
            return key, file_name
        else:
            x = 0
            while x < sinfo.MAX_EPONYMOUS_FILES:
                if x == sinfo.MAX_EPONYMOUS_FILES - 2:
                    new_file_name = rgen.generate_md5_str()
                    break
                new_file_name = ""
                iter_file_name = self.select("file", "name", f"name='{file_name}' AND owner={self._uid}").fetchall()
                if iter_file_name:
                    new_file_name = iter_file_name[0][0] + str(x)
                    if not self.is_file_exist(new_file_name):
                        break
                else:
                    new_file_name = rgen.generate_md5_str()
                x += 1
            self.insert(
                table="file",
                column_name="key, owner, status, name, load_time, deletion_time, file_type",
                values=f"'{key}', {self._uid}, 0, '{new_file_name}', {itime()}, -1, '{file_type}'"
            )

            return key, new_file_name

    def delete_file(self, key):
        if self.is_key_exist(key):
            if not self.select("file", "status", f"key='{key}'").fetchall()[0][0]:
                try:
                    shutil.move(f"user_files/{key}", "user_files/.deleted/")
                except shutil.Error:
                    print(tmsg.LOG_WARNING, shutil.Error)
                self.update("file", "status", "1", f"key='{key}'")
                return True
            else:
                return False

    def kill_file(self, key):
        if self.is_key_exist(key):
            match int(self.select("file", "status", f"key='{key}'").fetchall()[0][0]):
                case 1:
                    try:
                        #                                  anti hack protection
                        os.remove(f"./user_files/.deleted/{self.get_file_key(self.get_file_name(key))}")
                        self.update("file", "status", "-1", f"key='{key}'")
                    except FileNotFoundError:
                        return None  # file not found
                    return True  # file killed
                case -1:
                    return False  # file already killed
                case _:
                    self.delete_file(key)
                    self.kill_file(key)


import sqlite3
import time
import random_generator as rgen
import math
import server_info as sinfo
import shutil
import os
import messages as tmsg
import check_allowed_symbols as cas
from other_functions import megabytes


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
        if tg_id == -1:
            tg_id = self._tg_id
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
            return sinfo.DEFAULT_CHANGE_TIME  # default user
        case 1:
            return sinfo.PREMIUM_CHANGE_TIME  # premium user
        case 2:
            return 0                          # administrator
        case _:
            return 0                          # other


def get_time_to_update(level, seconds):
    days = level_time(level)
    return (86400 * days) - seconds


class DBConnection(Connection):
    def __init__(self, telegram_id=0, path=DB):
        super().__init__(telegram_id, path)
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
        """
        0 - link deactivated;
        1 - link activated.
        """
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
        """
        0 - user;
        1 - premium;
        2 - administrator.
        """
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

    def is_slink_exist(self, slink):
        check_slink = self.select("user", "super_link", f"super_link='{slink}'").fetchall()
        # DO NOT CHANGE == TO is !!!
        if check_slink == []:
            return False
        else:
            return True

    def is_link_exist(self, link):
        check_slink = self.select("user", "link", f"link='{link}'").fetchall()
        # DO NOT CHANGE == TO is !!!
        if check_slink == []:
            return False
        else:
            return True

    def change_slink(self, new):
        """
        0 - successful change;
        1 - error: link alredy exist;
        2 - empty slink;
        3 - forbidden sybols;
        4 - very long link;
        5 - very short link.
        """
        if new == "":
            return 2
        if not cas.check_slink(new):
            return 3
        if len(new) > sinfo.MAX_SLINK_LENGTH:
            return 4
        if not(len(new) >= sinfo.MIN_SLINK_LENGTH or self.level() == 2):
            return 5
        if self.is_slink_exist(new) or self.is_link_exist(new):
            return 1
        else:
            self.update("user", "super_link", f"'{new}'", f"telegram={self._tg_id}")
            return 0

    def delete_slink(self, uid=-1):
        """
        0 - success;
        1 - not exist id;
        2 - NULL (None) link.
        """
        if uid == -1:
            uid = self.get_id()
        if self.not_exist_id(uid):
            return 1
        if self.select("user", "super_link", f"id={uid}").fetchall()[0][0] is None:
            return 2
        self.update("user", "super_link", "NULL", f"id={uid}")
        return 0

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

    def is_banned(self, uid=-1):
        if uid == -1:
            uid = self.get_id()
        tg_id = self._tg_id
        return bool(self.select("user", "ban", f"id={uid}").fetchall()[0][0])

    # ADMINISTARATOR FUNCTIONS
    def ban(self, db_id, reason="no reason"):
        """
        0 - user not exist;
        1 - user is successfully BANNED;
        2 - already banned;
        3 - you dont have permissions;
        4 - incorrect reason.
        """
        if self.level() != 2:
            return 3
        if self.not_exist_id(db_id):
            return 0
        if self.select("user", "ban", f"id={db_id}").fetchall()[0][0] == 1:
            return 2

        backup = self.exec(
            f""" SELECT * FROM user WHERE id={db_id} """
        ).fetchall()[0]

        backup = str(list(backup)).replace('None', 'NULL')[1:-1]

        try:
            ban_id = self.exec(
                """SELECT ban_id FROM before_ban ORDER BY ban_id DESC LIMIT 1"""
            ).fetchall()[0][0]+1
        except sqlite3.OperationalError:
            ban_id = 1

        if reason.count("'") > 0:
            return 4

        self.exec(
            f""" INSERT INTO before_ban VALUES ({ban_id}, {itime()}, '{reason}', {backup})"""
        )

        self.update("user", "ban, activate_link, super_link, link, level", "1, 0, NULL, 'defalut', 0", f"id={db_id}")
        return 1

    def unban(self, db_id):
        """
        0 - user not exist;
        1 - user is successfully unbanned;
        2 - already unbanned.
        """
        if self.level() != 2:
            return 3
        if self.not_exist_id(db_id):
            return 0
        if self.select("user", "ban", f"id={db_id}").fetchall()[0][0] == 0:
            return 2
        self.update("user", "ban, link", f"0, '{rgen.generate_md5_str()}'", f"id={db_id}")
        return 1

    # def user_deleted(self, uid):
    #     return self.select("user", "")

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
        super().__init__(telegram_id, path)
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
        raw = self.select("file", "key", f"owner={self._uid} AND status=0").fetchall()
        if raw == []:
            return raw
        for x in raw:
            list_of_files.append(x[0])
        return list_of_files

    def file_names_list(self):
        list_of_files = []
        list_of_names = []
        for x in self.select("file", "key", f"owner={self._uid} AND status=0").fetchall():
            list_of_files.append(x[0])
        for x in list_of_files:
            list_of_names.append(self.select("file", "name", f"key='{x}'").fetchall()[0][0])
        self.used_space(self._uid)
        return list_of_names

    def can_load_new_file(self, lvl):
        min_delta = 0
        match lvl:
            case 0:
                min_delta = sinfo.USER_LTIME
            case 1:
                min_delta = sinfo.PREMIUM_LTIME
            case 2:
                min_delta = sinfo.ADMINISTRATOR_LTIME
        last_load_time = self.select("user", "file_load_time", f"telegram={self._tg_id}").fetchall()[0][0]
        now = itime()
        if now - last_load_time >= min_delta:
            return True, 0
        else:
            return False, min_delta - (now - last_load_time)

    def get_file_name(self, key):
        if self.is_key_exist(key):
            return self.select("file", "name", f"key='{key}'").fetchall()[0][0]

    def full_files_list(self):
        list_of_files = []
        list_of_status = []
        raw_key = self.select("file", "key", f"owner={self._uid}").fetchall()
        raw_status = self.select("file", "status", f"owner={self._uid}").fetchall()
        if raw_key == []:
            list_of_files = raw_key
        else:
            for x in raw_key:
                list_of_files.append(x[0])
        if raw_status == []:
            list_of_status = raw_status
        else:
            for x in raw_status:
                list_of_status.append(x[0])
        return list_of_files, list_of_status

    def select_file(self, key):
        self.update("user", "selected_file", f"'{key}'", f"telegram={self._tg_id}")

    def get_selected_file(self, uid=-1):
        if uid == -1:
            uid = self._uid
        sf = self.select("user", "selected_file", f"id={uid}").fetchall()
        if sf is None:
            return None
        else:
            return sf[0][0]

    def used_space(self, uid=-1):
        if uid == -1:
            uid = self._uid
        mb_list = self.select("file", "mb_size", f"owner={uid} AND status=0").fetchall()
        mb = 0.0
        for x in mb_list:
            mb += x[0]
        self.update("user", "mb_total", mb, f"id={uid}")
        return mb

    def get_file_type(self, key="default", name="default"):
        if key == "defalut": key = self.get_file_key(name)
        if self.is_key_exist(key):
            return self.select("file", "file_type", f"key='{key}'").fetchall()[0][0]

    def remove_file_by_number(self, num, uid=-1):
        """
                0 - succed;
                1 - no files;
                2 - out of range
                """
        if uid == -1:
            uid = self._uid
        load_time = []
        flist = self.files_list()
        # DO NO CHANGE == TO is
        if flist == []:
            self.update("user", "mb_total", 0.0, f"id={uid}")
            return 1
        if num > len(flist) or num < 1:
            return 2
        self.delete_file(flist[num-1])
        return 0

    def remove_oldest_file(self, uid=-1):
        """
        0 - succed;
        1 - no files
        """
        if uid == -1:
            uid = self._uid
        load_time = []
        flist = self.files_list()
        # DO NO CHANGE == TO is
        if flist == []:
            self.update("user", "mb_total", 0.0, f"id={uid}")
            return 1
        for f in flist:
            load_time.append(self.select("file", "load_time", f"owner={uid}").fetchall()[0][0])
        temp = min(load_time)
        res = [i for i, j in enumerate(load_time) if j == temp]
        self.delete_file(flist[res[0]])
        return 0

    def file_count(self, uid=-1):
        if uid == -1:
            uid = self._uid
        return len(self.select("file", "status", f"status=0 AND owner={uid}").fetchall())

    def add_mb_total(self, mb, lvl):
        """
        0 - succed;
        1 - file is too large;
        2 - no space.
        """
        if self.is_user_exist():
            now = self.select("user", "mb_total", f"id={self._uid}").fetchall()[0][0]
            if mb > megabytes(lvl):
                return 1
            if now+mb > megabytes(lvl):
                if self.remove_oldest_file():
                    return 2
                self.add_mb_total(mb, lvl)
                now = self.select("user", "mb_total", f"id={self._uid}").fetchall()[0][0]
                self.update("user", "mb_total", now + mb, f"id={self._uid}")
                return 0
            else:
                self.add_mb_traffc(mb)
                self.update("user", "mb_total", now+mb, f"id={self._uid}")

    def add_mb_traffc(self, mb):
        if self.is_user_exist() and mb > 0.0:
            now = self.select("user", "mb_traffic", f"id={self._uid}").fetchall()[0][0]
            self.update("user", "mb_traffic", str(now+mb), f"id={self._uid}")

    def rename_file(self, key, new_name):
        """
        0 - succed;
        1 - error.
        """
        if self.is_key_exist(key):
            self.update("file", "name", f"'{new_name}'", f"key='{key}'")
            return 0
        return 1

    def new_file(self, file_name, file_type, file_size=0.1, lvl=0):
        can_list = self.can_load_new_file(lvl)
        if can_list[0]:
            pass
        else:
            return None, None, can_list[1]
        key = rgen.generate_md5_str()
        fsn = cas.file_safe_name(file_name)
        if self.add_mb_total(file_size, lvl):
            return None, None
        self.update("user", "file_load_time", itime(), f"telegram={self._tg_id}")
        match lvl:
            case 0:
                max_count = sinfo.USER_FILE_COUNT
            case 1:
                max_count = sinfo.PREMIUM_FILE_COUNT
            case 2:
                max_count = sinfo.ADMINISTRATOR_FILE_COUNT
        if self.file_count() > max_count:
            [self.remove_oldest_file() for i in range(self.file_count() - max_count + 1)]
        if not self.get_path_to_file(fsn):
            # if user dont have two or comre files with same names
            # yeas, my English B)
            self.insert(
                table="file",
                column_name="key, owner, status, name, load_time, kill_time, file_type, mb_size",
                values=f"'{key}', {self._uid}, 0, '{fsn}', {itime()}, -1, '{file_type}', {file_size}"
            )
            return key, fsn
        else:
            x = 0
            new_file_name = ""
            while x < sinfo.MAX_EPONYMOUS_FILES:
                if x == sinfo.MAX_EPONYMOUS_FILES - 2:
                    new_file_name = rgen.generate_md5_str()
                    break
                new_file_name = ""
                iter_file_name = self.select("file", "name", f"name='{fsn}' AND owner={self._uid}").fetchall()
                if iter_file_name:
                    new_file_name = iter_file_name[0][0] + str(x)
                    if not self.is_file_exist(new_file_name):
                        break
                else:
                    new_file_name = rgen.generate_md5_str()
                x += 1
            self.insert(
                table="file",
                column_name="key, owner, status, name, load_time, kill_time, file_type, mb_size",
                values=f"'{key}', {self._uid}, 0, '{new_file_name}', {itime()}, -1, '{file_type}', {file_size}"
            )
            return key, new_file_name

    def delete_file(self, key):
        if self.is_key_exist(key):
            if not self.select("file", "status", f"key='{key}'").fetchall()[0][0]:
                try:
                    shutil.move(f"{sinfo.PATH_TO_FILES}{key}", f"{sinfo.PATH_TO_DELETED}")
                except Exception as e:
                    print(tmsg.LOG_WARNING, str(e))
                self.update("file", "status", "1", f"key='{key}'")
                uid = self.select("file", "owner", f"key='{key}'").fetchall()[0][0]
                self.used_space(uid)
                return True
            else:
                return False

    def kill_file(self, key):
        """
        True - file killed;
        False - file already killed;
        None - file not found.
        """
        if self.is_key_exist(key):
            match int(self.select("file", "status", f"key='{key}'").fetchall()[0][0]):
                case 1:
                    try:
                        #                                  anti hack protection
                        os.remove(f"{sinfo.PATH_TO_DELETED}{self.get_file_key(self.get_file_name(key))}")
                        self.update("file", "status", "-1", f"key='{key}'")
                    except FileNotFoundError:
                        return None
                    return True
                case -1:
                    return False
                case _:
                    self.delete_file(key)
                    self.kill_file(key)


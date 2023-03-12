import sqlite3
import time
import random_generator as rgen


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


class DBConnection:
    def __init__(self, telegram_id=0, path="./db/user.db"):
        self._db_link = path  # Path to database
        self._tg_id = str(telegram_id)
        self._con = sqlite3.connect(self._db_link)
        self._cur = self._con.cursor()
        if self.not_exist_telegram():
            self._md5_link = rgen.generate_md5_str()
        else:
            self._md5_link = self.get_md5()

    def __del__(self):
        self._con.close()

    def info(self):
        return f"db_link={self._db_link}\n_tg_id={self._tg_id}"

    def connection(self):
        return self._con

    def exec(self, command):
        return self._cur.execute(command)

    #    def change_id_to(self, telegram_id=0):
    #        self._tg_id = telegram_id

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

    def get_md5(self):
        if self.not_exist_telegram():
            self.new_user()
            return self.get_md5()
        else:
            return self.select(table="user",
                               result_column="link",
                               expr=f"telegram={self._tg_id}").fetchall()[0][0]

    def not_exist_telegram(self):
        if not self.select("user", "telegram", f"telegram={self._tg_id}").fetchall():
            return True
        else:
            return False

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
            match int(
                self.select(table="user", result_column="level", expr=f"telegram={self._tg_id}").fetchall()[0][0]):
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

    def new_link(self):
        ...

    def new_user(self):
        self.insert(table="user",
                    column_name="""link, level, reg_time, mb_total, telegram, ban, title, mb_traffic,
                                   deactivate_link, link_time, click, link_log""",
                    values=f"""'{self._md5_link}', 0, {itime()}, 0.0, {self._tg_id}, 0, 'My Page', 0.0,
                                0, {itime()}, 0, '{self._md5_link}'""")

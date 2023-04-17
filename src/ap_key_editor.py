#!/usr/bin/python3

import sqlite3
import random
import colorama as cl

ALPHABET = "qwertyuiopasdfghjklzxcvbnm01234567890"


def check_key(key):
    # False - check failed
    if len(key) == 8:
        return all(c in ALPHABET for c in key)
    else:
        return False


class APConnection:
    def __init__(self, DB="./db/web.db"):
        self._con = sqlite3.connect(DB)
        self._cur = self._con.cursor()

    def __del__(self):
        self._con.close()

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

    def delete(self, table, condition):
        self.exec(
            """ DELETE FROM %(table)s WHERE %(condition)s"""
            % {'table': table, 'condition': condition}
        )
        self._con.commit()


def generate_key():
    return "%008x" % random.getrandbits(32)


def watch_keys():
    apc = APConnection()
    raw = apc.select("key", "key", "1").fetchall()
    key_list = []
    for i in range(len(raw)):
        key_list.append(raw[i][0])

    # DO NOT CHANGE TO "is"
    if not key_list:
        print("There are no keys")
    else:
        print("Access keys: "+str(key_list)[1:-1])


def help_msg():
    print(f"""\
Commands:

{cl.Fore.YELLOW}exit{cl.Style.RESET_ALL} - command for safe exit
{cl.Fore.GREEN}watchkey{cl.Style.RESET_ALL} - list of all keys
{cl.Fore.GREEN}addkey{cl.Style.RESET_ALL}\t[key1 key2 ...] - add new key(s)
{cl.Fore.GREEN}rmkey{cl.Style.RESET_ALL}\t[key1 key2 ...] - removes the key(s)
{cl.Fore.GREEN}genkey{cl.Style.RESET_ALL}\t[number] - generates n key(s)
{cl.Fore.YELLOW}rmall{cl.Style.RESET_ALL} - deleting all keys
""")


def add_key(cmd):
    if len(cmd) < 2:
        print("Enter the keys!")
        return
    new = []
    for k in range(len(cmd)-1):
        new.append(cmd[k+1])

    apc = APConnection()
    for k in new:
        if check_key(k):
            if not apc.select("key", "key", f"key='{k}'").fetchall():
                apc.insert("key", "key", f"'{k}'")
                print(f"{cl.Fore.GREEN}Key added:{cl.Style.RESET_ALL} " + f"'{k}'")
            else:
                print(f"{cl.Fore.YELLOW}Key already exist:{cl.Style.RESET_ALL} " + f"'{k}'")
        else:
            print(f"{cl.Fore.RED}Incorrect key:{cl.Style.RESET_ALL} " + f"'{k}'")
    return


def rm_key(cmd):
    if len(cmd) < 2:
        print("Enter the keys!")
        return
    new = []
    for k in range(len(cmd)-1):
        new.append(cmd[k+1])

    apc = APConnection()
    for k in new:
        if check_key(k):
            if not apc.select("key", "key", f"key='{k}'").fetchall():
                print(f"{cl.Fore.RED}Key not found:{cl.Style.RESET_ALL} " + f"'{k}'")
            else:
                apc.delete("key", f"key='{k}'")
                print(f"{cl.Fore.YELLOW}Key removed:{cl.Style.RESET_ALL} " + f"'{k}'")
        else:
            print(f"{cl.Fore.RED}Incorrect key:{cl.Style.RESET_ALL} " + f"'{k}'")
    return


def gen_key(cmd):
    if len(cmd) < 2:
        print("Enter the number!")
        return
    try:
        n = int(cmd[1])
        if n < 1:
            print(f"{cl.Fore.RED}Must be{cl.Style.RESET_ALL} n > 0")
        elif n > 256:
            print(f"{cl.Fore.RED}Must be{cl.Style.RESET_ALL} n < 256")

        for i in range(n):
            add_key([0, generate_key()])

    except ValueError:
        print(f"{cl.Fore.RED}Incorrect number!{cl.Style.RESET_ALL}")


def rm_all():
    apc = APConnection()
    apc.delete("key", "1")
    print(f"{cl.Fore.YELLOW}All keys deleted{cl.Style.RESET_ALL}")


def main():
    cl.init()
    cl.just_fix_windows_console()
    help_msg()
    print()
    try:
        while True:
            cmd = input(cl.Fore.CYAN + "> " + cl.Style.RESET_ALL).split(" ")
            match cmd[0]:
                case "watchkey":
                    watch_keys()
                case "help":
                    help_msg()
                case "addkey":
                    add_key(cmd)
                case "rmkey":
                    rm_key(cmd)
                case "genkey":
                    gen_key(cmd)
                case "rmall":
                    rm_all()
                case "exit":
                    print(f"\n{cl.Fore.GREEN}Exit")
                    exit(0)
            print()
    except KeyboardInterrupt:
        print(f"\n\n{cl.Fore.RED}Emergency exit{cl.Style.RESET_ALL} (do not recommend using this command)")
        exit(1)


if __name__ == "__main__":
    main()

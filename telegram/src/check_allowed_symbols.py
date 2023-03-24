from server_info import SLINK_SYMBOLS, FILE_SYMBOLS


def check_slink(slink):
    # False - check failed
    return all(c in SLINK_SYMBOLS for c in slink)


def file_safe_name(file_name):
    out = ""
    for i in file_name:
        if i in FILE_SYMBOLS:
            out += i
        else:
            out += "_"
    return out

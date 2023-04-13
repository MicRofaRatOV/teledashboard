from server_info import SLINK_SYMBOLS, FILE_SYMBOLS, MAX_FILE_NAME_LENGTH


def check_slink(slink):
    # False - check failed
    return all(c in SLINK_SYMBOLS for c in slink)


def file_safe_name(file_name):
    if len(file_name) > MAX_FILE_NAME_LENGTH:
        file_name = file_name[:32]
    out = ""
    for i in file_name:
        if i in FILE_SYMBOLS:
            out += i
        else:
            out += "_"
    return out

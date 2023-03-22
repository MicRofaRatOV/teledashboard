SLINK_SYMBOLS = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789_"


def check_slink(slink):
    global SLINK_SYMBOLS
    # False - check failed
    return all(c in SLINK_SYMBOLS for c in slink)

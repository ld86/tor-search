import logging
import sys


def getLogger():
    root = logging.getLogger("logger")
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    return root

log = getLogger().info

import os
import logging
import shutil
import datetime


def remove_file(file):
    logger1 = logging.getLogger("PTL.FileHandler")
    if os.path.isfile(file):
        try:
            os.remove(file)
        except:
            logger1.error("cannot remove: " + file)
            return 1
        return 0
    return 0


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    return 0


def backup_file(filename, backup_filelocation, makeDated=True):
    ensure_dir(backup_filelocation)
    base, old_name = os.path.split(filename)
    date_tag = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_name = old_name
    if makeDated:
        new_name = date_tag + '_' + old_name
    shutil.copy(filename, os.path.join(backup_filelocation,  new_name))
    return 0


def replace_comma(string_with_comma):
    a = float(string_with_comma.replace(',', '.'))
    return a


def file_modification_date(filename):
    """

    :param filename: input file
    :return: the modification date of a file
    """
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
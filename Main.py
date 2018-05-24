from settings import Settings as my_settings
from filelocations import FileLocations as Loc

import datetime
import time
import logging
import logging.config
import pickle
import os

from PTL import PTL_FileHandler


def backup_used_settings():
    # add any files you want to backup every time the tools runs
    file_list = ["Settings.ini",
                 "File_Locations.ini"
                 ]
    make_dated = True

    for file in file_list:
        PTL_FileHandler.backup_file(file, Loc.get_backup_directory(), make_dated)
    return 0


def check_pickle_exists(name):
    if os.path.isfile(Loc.pickle_folder + name + '.pickle'):
        return True
    else:
        return False


def new_pickle(name):
    """

    :param name: name of pickle
    :return: true when pickle cannot be used because it is old or does not exist.
    False when it can be used because it is from today
    """
    logger = logging.getLogger(__name__)
    if check_pickle_exists(name):
        pickle_date = PTL_FileHandler.file_modification_date(Loc.pickle_folder + name + '.pickle').date()
        if pickle_date == datetime.date.today():
            logger.info('Pickle data %s is from today' % name)
            return False
        else:
            logger.info('pickle %s is old. Data loaded from source.' % name)
            return True
    else:
        logger.info('pickle %s does not exist. Data loaded from source.' % name)
        return True


def get_data():
    return 0


def save_pickle(data_set, name):
    """"Save object in pickle with filename name """
    logger = logging.getLogger(__name__)
    with open(Loc.pickle_folder + name + '.pickle', 'wb') as f:
        pickle.dump(data_set, f)
        logger.info("saved pickle " + name)
    return 0


def load_pickle(name):
    logger = logging.getLogger(__name__)
    with open(Loc.pickle_folder + name + '.pickle', "rb") as file:
        logger.info("load pickle " + name)
        pickle_object = pickle.load(file)
    return pickle_object


def run(capture_date=datetime.datetime.today().date()):
    logger = logging.getLogger(__name__)

    start_time = time.time()
    logger.info(str(round(time.time() - start_time)) + " read data")

    # read functions
    if my_settings.run_only_pickles:
        logger.info("only pickles used")
    data = get_data()

    # check data

    # set up functions to check whether data is good

    # calculations
    logger.info("start calculations")
    a = 5
    print("a = %s" % a)

    # check calculations to be consistent

    # export
    logger.info('start exports')

    # finishing
    time_elapsed = round(time.time() - start_time)
    logger.info("%ss finished run" % str(time_elapsed))
    return 0


def main():
    my_settings.fill_settings()
    Loc.fill_file_locations()
    PTL_FileHandler.ensure_dir(Loc.log_folder)
    PTL_FileHandler.ensure_dir(Loc.pickle_folder)
    logDateTag = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = Loc.log_folder + Loc.log_file_name + "_%s.log" % logDateTag
    logging.config.fileConfig("logging.conf", defaults={'logfilename': log_file})
    Loc.set_log_location(log_file)
    # create Logger
    logger = logging.getLogger(__name__)
    logger.info("user: {} on computer: {}".format(os.getlogin(), os.environ['COMPUTERNAME']))

    backup_used_settings()

    # by default, today's capture date is run. You can fill in any days ago
    capture_date = datetime.date.today() - datetime.timedelta(days=my_settings.run_days_ago)
    logger.info('start run with capture date = %s' % str(capture_date))
    try:
        run(capture_date)
    except FileNotFoundError:
        logger.exception('Run stopped')
    except:
        logger.exception('Run failed')
        raise
    logger.info('finished switch')
    return 0


if __name__ == '__main__':
    main()
    pass

import configparser
import logging


def singleton(cls):
    return cls()


@singleton
class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.run_only_pickles = None
        self.force_new_data = None
        self.run_days_ago = None
        self.transcillary_date_format = None

        self.mail_send = None
        self.mail_from = None
        self.mail_start_to = None
        self.mail_start_cc = None
        self.mail_end_to = None
        self.mail_end_cc = None
        self.mail_error_to = None
        self.mail_error_cc = None

    def fill_settings(self):
        logger = logging.getLogger(__name__)
        self.config.read('Settings.ini')

        self.run_only_pickles = self.config.getboolean('run', 'run_only_pickles')
        self.run_days_ago = self.config.getboolean('run', 'run_days_ago')
        self.force_new_data = self.config.getboolean('run', 'force_new_data')

        # read some dictionaries


def get_dict_from_config(config, section_name):
    dictionary = {}
    for key in config[section_name]:
        k1, k2 = key.split('_')
        if (k1, k2) not in dictionary:
            dictionary[(k1, k2)] = config.getint(section_name, key)
    return dictionary

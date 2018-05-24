import os
import logging
import configparser
import datetime

import PTL.PTL_FileHandler


def singleton(cls):
    return cls()


@singleton
class FileLocations:
    def __init__(self):
        self.extensiontemp = None
        self.input_directory_default_folder = None
        self.log_file_name = None
        self.log_folder = None
        self.log_file_full_path_location = None
        self.pickle_folder = None

        self.export_directory = None
        self.backup_directory = None
        self.log_folder_fixed = None

        self.input_something_file_name = None

    def fill_file_locations(self):
        config = configparser.ConfigParser()
        config.read('File_Locations.ini')

        self.extensiontemp = config.get('default', 'extensiontemp')
        self.input_directory_default_folder = config.get('input', 'input_directory_default_folder')

        self.log_file_name = config.get('default', 'log_file_name')
        self.log_folder = config.get('default', 'log_folder')
        self.log_file_full_path_location = config.get('default', 'log_fixed_folder')
        self.pickle_folder = config.get('default', 'pickle_folder')

        self.input_something_file_name = config.get('input', 'input_something_file_name')

        # export file names

        # export folders
        self.export_directory = config.get('export', 'export_directory')
        self.backup_directory = config.get('export', 'backup_directory')

    # extra locations
    def set_log_location(self, log_file_location):
        if self.log_file_full_path_location == '':
            file = os.getcwd() + os.path.sep + log_file_location
        else:
            file = self.log_file_full_path_location + log_file_location
        self.log_folder_fixed = file

    def get_full_path_log_location(self):
        if self.log_folder_fixed is None:
            return ""
        else:
            return self.log_folder_fixed

    def set_working_directory(self, directory):
        self.input_directory_default_folder = directory

    ########## Imports #####

    # input file name

    # input files (folder + file names)
    def input_something_file(self):
        folder = self.input_directory_default_folder
        return os.path.join(folder, self.input_something_file_name)

    ########## Exports #####

    # file names

    def get_backup_directory(self):
        folder = self.backup_directory
        if folder == '':
            folder = self.input_directory_default_folder + '/used_settings/'
        PTL.PTL_FileHandler.ensure_dir(folder)
        return folder


def get_list_from_config(config, section_name, field_name):
    result = [e.strip() for e in config.get(section_name, field_name).split(',')]
    return result

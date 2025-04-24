from Sorter import Sorter
from DataHandler import DataHandler
from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_NAME_2, YEAR, DESCRIPTION,
    FILES_ID, TARGET_ID, BROWSER_ID)

import logging
import re

class Controller:

    def __init__(self):
        logging.debug("Init Controller")
        self.dataHandler = DataHandler()
        self.dataHandler.load_settings()
        self.dataHandler.update()
        self.sorter = Sorter(file_path=self.dataHandler.get_file_path(),
                             target_path=self.dataHandler.get_target_path())
        self.observers = [self.dataHandler, self.sorter]

    def new_observer(self, observer):
        self.observers.append(observer)

    def set_observer_filepath(self, path):
        logging.debug(f"Setting file path to {path} for all observers")
        for observer in self.observers:
            logging.debug(f"observer:{observer} to file path:{path}")
            observer.set_file_path(path)
            observer.update()

    def set_observer_targetpath(self, path):
        logging.debug(f"Setting target path to {path} for all observers")
        for observer in self.observers:
            logging.debug(f"observer:{observer} to target path:{path}")
            observer.set_target_path(path)
            observer.update()

    def create_logs(self):
        pass #logs when application closes

    def get_data_copy(self):
        return self.dataHandler.get_data_copy()

    def get_row(self, file_name):
        return self.dataHandler.get_row(file_name)

    def open_file(self, file_name):
        self.dataHandler.open_file(file_name)

    def get_path(self, pathID):
        match pathID:
            case _ if pathID == FILES_ID:
                path = self.dataHandler.get_file_path()
            case _ if pathID == TARGET_ID:
                path = self.dataHandler.get_target_path()
            case _ if pathID == BROWSER_ID:
                path = self.dataHandler.get_browser_path()
            case _:
                logging.exception(f"pathID invalid:{pathID}")
                raise ValueError("Invalid pathID passed into controller.get_path()")

        if path is None:
            return ""
        else:
            return path

    def set_path(self, pathID, path):
        if path == '':
            logging.warning("called with empty path, no action taken from controller")
            return
        match pathID:
            case _ if pathID == FILES_ID:
                self.set_observer_filepath(path)
            case _ if pathID == TARGET_ID:
                self.set_observer_targetpath(path)
            case _ if pathID == BROWSER_ID:
                self.dataHandler.set_browser_path(path)

    def save_settings(self):
        self.dataHandler.save_settings()

    def get_resource(self, relative_path):
        return self.dataHandler.resource_path(relative_path)

    def get_base_directory(self):
        return self.dataHandler.get_base_directory()

    def save_row_changes(self, tab_type, file_data):
        """
        VALID_NAME_CLIENT = r"[A-Z][a-z]*"
        VALID_NAME_BUSINESS = r"([A-Z]+ )+(LLC|INC)"
        VALID_YEAR = r"\d{4}"

        needs_fixed = []
        def save_client():
            client1_first_name = self.client1_first_entry.get()
            valid_first_name = re.match(self.VALID_NAME_CLIENT, client1_first_name)
            client1_last_name = self.client1_last_entry.get()
            valid_last_name = re.match(self.VALID_NAME_CLIENT, client1_last_name)
            if valid_first_name and valid_last_name:
                client1_full_name = client1_first_name + " " + client1_last_name
                self.file_data[self.CLIENT_NAME] = client1_full_name
            else:
                needs_fixed.append("Client 1")

            has_client2 = self.client_radio_var.get() == 1
            if has_client2:
                client2_first_name = self.client2_first_entry.get()
                valid_first_name = re.match(self.VALID_NAME_CLIENT, client2_first_name)
                client2_last_name = self.client2_last_entry.get()
                valid_last_name = re.match(self.VALID_NAME_CLIENT, client2_last_name)

                if valid_first_name and valid_last_name:
                    client2_full_name = client2_first_name + " " + client2_last_name
                    self.file_data[self.CLIENT_NAME_2] = client2_full_name
                else:
                    needs_fixed.append("Client 2")

            year = self.client_year_entry.get()
            valid_year = re.match(self.VALID_YEAR,year)
            if valid_year:
                self.file_data[self.YEAR] = int(year)
            else:
                needs_fixed.append("Year")

            file_desc = self.client_file_desc_entry.get()
            valid_desc = file_desc != ""
            if valid_desc:
                self.file_data[self.DESCRIPTION] = file_desc
            else:
                needs_fixed.append("File Description")

            if len(needs_fixed) > 0:
                return needs_fixed
            else:
                print(f"og:{self.file_data_original}")
                print(f"new:{self.file_data}")

        def save_business():
            client1_name = self.client1_entry.get()
            valid_name = re.match(self.VALID_NAME_BUSINESS, client1_name)
            if valid_name:
                self.file_data[self.CLIENT_NAME] = client1_name
            else:
                needs_fixed.append("Client 1")

            has_client2 = self.business_radio_var.get() == 1
            if has_client2:
                client2_name = self.client2_entry.get()
                valid_name = re.match(self.VALID_NAME_BUSINESS, client2_name)

                if valid_name:
                    self.file_data[self.CLIENT_NAME_2] = client2_name
                else:
                    needs_fixed.append("Client 2")

            year = self.business_year_entry.get()
            valid_year = re.match(self.VALID_YEAR, year)
            if valid_year:
                self.file_data[self.YEAR] = int(year)
            else:
                needs_fixed.append("Year")

            file_desc = self.business_file_desc_entry.get()
            valid_desc = file_desc != ""
            if valid_desc:
                self.file_data[self.DESCRIPTION] = file_desc
            else:
                needs_fixed.append("File Description")

        if self.tab_view.get() == "Client":
            save_client()
        else:
            save_business()
        """

    #temp functions
    def save_data(self):
        self.dataHandler.save_data_instance()

    def load_data(self):
        self.dataHandler.load_data_instance()

    def check_data(self):
        print(self.dataHandler.get_data_copy())

    def filter_data(self):
        self.dataHandler.filter_data()

    def get_settings(self):
        self.dataHandler.load_settings()
from typing import TypedDict
import pandas as pd

#files dataframe
FILE_NAME = 'File_Name'
STATUS = 'File_Status'
CLIENT_TYPE = 'Client_Type'
CLIENT_NAME = 'Client_Name'
CLIENT_2_NAME = 'Client_2_Name'
YEAR = 'Year'
DESCRIPTION = 'File_Description'

DEFAULT_DATAFRAME = pd.DataFrame({
    FILE_NAME:pd.Series(dtype=str),
    STATUS:pd.Series(dtype=bool),
    CLIENT_TYPE:pd.Series(dtype=str),
    CLIENT_NAME:pd.Series(dtype=str),
    CLIENT_2_NAME:pd.Series(dtype=str),
    YEAR:pd.Series(dtype=int),
    DESCRIPTION:pd.Series(dtype=str)
})

DEFAULT_VALUES = {
    FILE_NAME: "",
    STATUS: False,
    CLIENT_TYPE: 'unknown',
    CLIENT_NAME: 'unknown client',
    CLIENT_2_NAME: None,
    YEAR: -1,
    DESCRIPTION: None
}

CLIENT = "Client"
BUSINESS = "Business"

INCOME_TAX = "Income Tax"

#settings & file paths
FILES_ID = "files"
TARGET_ID = "target"

DEFAULT_SETTINGS = {
    FILES_ID: "",
    TARGET_ID: ""
}

#data validation
VALID_NAME_CLIENT = r"[A-Z][a-z]* [A-Z][a-z]*"
VALID_NAME_BUSINESS = r"([A-Z0-9]+ )+[A-Z]{3}"
VALID_YEAR = r"\d{4}"

NAME_VALIDATORS = {
            CLIENT: VALID_NAME_CLIENT,
            BUSINESS: VALID_NAME_BUSINESS
        }

class FileData(TypedDict):
    File_Name: str
    File_Status: bool
    Client_Type: str
    Client_Name: str
    Client_2_Name: str
    Year: int
    File_Description: str

#UI Navigation
HOME_ID = "home"
SETTINGS_ID = "settings"
HELP_ID = "help"
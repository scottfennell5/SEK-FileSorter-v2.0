from typing import TypedDict

FILE_NAME = 'File_Name'
STATUS = 'File_Status'
CLIENT_TYPE = 'Client_Type'
CLIENT_NAME = 'Client_Name'
CLIENT_2_NAME = 'Client_2_Name'
YEAR = 'Year'
DESCRIPTION = 'File_Description'

class FileData(TypedDict):
    File_Name: str
    File_Status: bool
    Client_Type: str
    Client_Name: str
    Client_2_Name: str
    Year: int
    File_Description: str

DEFAULT_VALUES = {
    FILE_NAME: "",
    STATUS: False,
    CLIENT_TYPE: 'unknown',
    CLIENT_NAME: 'unknown client',
    CLIENT_2_NAME: None,
    YEAR: -1,
    DESCRIPTION: None
}

FILES_ID = "files"
TARGET_ID = "target"
BROWSER_ID = "browser"

CLIENT = "Client"
BUSINESS = "Business"

VALID_NAME_CLIENT = r"[A-Z][a-z]* [A-Z][a-z]*"
VALID_NAME_BUSINESS = r"([A-Z]+ )+(LLC|INC)"
VALID_YEAR = r"\d{4}"

NAME_VALIDATORS = {
            CLIENT: VALID_NAME_CLIENT,
            BUSINESS: VALID_NAME_BUSINESS
        }
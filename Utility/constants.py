FILE_NAME = 'File_Name'
STATUS = 'File_Status'
CLIENT_TYPE = 'Client_Type'
CLIENT_NAME = 'Client_Name'
CLIENT_NAME_2 = 'Client_Name_2'
YEAR = 'Year'
DESCRIPTION = 'File_Description'

DEFAULT_VALUES = {
    FILE_NAME: "",
    STATUS: False,
    CLIENT_TYPE: 'unknown',
    CLIENT_NAME: 'unknown client',
    CLIENT_NAME_2: None,
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
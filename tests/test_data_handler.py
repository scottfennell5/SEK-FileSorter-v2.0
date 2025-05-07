import os
import tempfile
import yaml
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.DataHandler import DataHandler
from src.Utility.constants import (
    FILE_NAME, STATUS, CLIENT_NAME, CLIENT_2_NAME,
    CLIENT_TYPE, YEAR, DESCRIPTION, DEFAULT_VALUES,
    DEFAULT_DATAFRAME, DEFAULT_SETTINGS, FileData,
    FILES_ID, TARGET_ID
)


@pytest.fixture
def temp_data_handler(tmp_path):
    # Mock resource_path to always return a path inside tmp_path
    with patch.object(DataHandler, 'resource_path', side_effect=lambda rel: tmp_path / os.path.basename(rel)):
        handler = DataHandler()
        yield handler

def test_validate_settings_valid(temp_data_handler):
    valid = {
        FILES_ID: "/some/path",
        TARGET_ID: "/another/path"
    }
    assert temp_data_handler.validate_settings(valid)

def test_validate_settings_missing_key(temp_data_handler):
    invalid = {FILES_ID: "/path"}
    assert not temp_data_handler.validate_settings(invalid)

def test_validate_settings_unexpected_key(temp_data_handler):
    invalid = {**DEFAULT_SETTINGS, "EXTRA_KEY": "unexpected"}
    assert not temp_data_handler.validate_settings(invalid)

def test_apply_settings_invalid_paths(temp_data_handler):
    settings = {
        FILES_ID: "/nonexistent1",
        TARGET_ID: "/nonexistent2"
    }
    temp_data_handler.apply_settings(settings)
    assert temp_data_handler.file_path == ""
    assert temp_data_handler.target_path == ""

def test_save_and_load_settings(tmp_path):
    with patch.object(DataHandler, 'resource_path', side_effect=lambda rel: tmp_path / os.path.basename(rel)):
        handler = DataHandler()
        handler.file_path = "/files"
        handler.target_path = "/target"
        handler.browser_path = "/browser"
        handler.save_settings()

        # Load it back manually
        with open(tmp_path / "settings.yaml", "r") as f:
            settings = yaml.safe_load(f)
        assert settings[FILES_ID] == "/files"

def test_load_data_instance_creates_empty_if_missing(tmp_path):
    data_path = tmp_path / "olddata.yaml"

    handler = DataHandler.__new__(DataHandler)  # bypass __init__
    handler.olddata_path = str(data_path)
    handler.files_df = None

    handler.validate_file_dataframe = lambda: True

    handler.load_data_instance()

    assert data_path.exists()
    assert handler.files_df.equals(DEFAULT_DATAFRAME)

def test_validate_file_dataframe_good(temp_data_handler):
    df = pd.DataFrame([DEFAULT_VALUES])
    temp_data_handler.files_df = df
    assert temp_data_handler.validate_file_dataframe()

def test_validate_file_dataframe_with_unexpected_column(temp_data_handler):
    df = pd.DataFrame([{**DEFAULT_VALUES, "Extra": 1}])
    temp_data_handler.files_df = df
    assert not temp_data_handler.validate_file_dataframe()

def test_update_row_updates_existing(temp_data_handler):
    row = {**DEFAULT_VALUES, FILE_NAME: "test.pdf"}
    temp_data_handler.files_df = pd.DataFrame([row])
    updated = {
        FILE_NAME: "test.pdf", STATUS: True, CLIENT_NAME: "John Smith",
        CLIENT_2_NAME: "", CLIENT_TYPE: "Client", YEAR: 2022, DESCRIPTION: "Form"
    }
    temp_data_handler.update_row(updated)
    df = temp_data_handler.files_df
    assert df.at[0, CLIENT_NAME] == "John Smith"
    assert bool(df.at[0, STATUS]) is True

def test_open_file_path_undefined(temp_data_handler):
    temp_data_handler.file_path = ""
    result = temp_data_handler.open_file("foo.pdf")
    assert "File path undefined" in result

def test_get_row_returns_correct_data(temp_data_handler):
    row = {**DEFAULT_VALUES, FILE_NAME: "abc.pdf", CLIENT_NAME: "Jane"}
    temp_data_handler.files_df = pd.DataFrame([row])
    result = temp_data_handler.get_row("abc.pdf")
    assert result[CLIENT_NAME] == "Jane"

def test_get_row_not_found(temp_data_handler):
    temp_data_handler.files_df = pd.DataFrame([DEFAULT_VALUES])
    result = temp_data_handler.get_row("nonexistent.pdf")
    assert result is None

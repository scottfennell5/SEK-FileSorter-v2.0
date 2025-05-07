import os
import pandas as pd
import pytest
from unittest.mock import patch

from Core.Sorter import Sorter  # Replace with actual import
from src.Utility.constants import (
    FILE_NAME, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,
    CLIENT, BUSINESS, INCOME_TAX
)

@pytest.fixture
def sample_data_client():
    return pd.DataFrame([{
        FILE_NAME: "file1.pdf",
        CLIENT_TYPE: CLIENT,
        CLIENT_NAME: "John Doe",
        CLIENT_2_NAME: "Jane Doe",
        YEAR: "2023",
        DESCRIPTION: "Form 1040"
    }])

@pytest.fixture
def sample_data_business():
    return pd.DataFrame([{
        FILE_NAME: "biz1.pdf",
        CLIENT_TYPE: BUSINESS,
        CLIENT_NAME: "TEST LLC",
        CLIENT_2_NAME: "AUX INC",
        YEAR: "2023",
        DESCRIPTION: "Invoice"
    }])

def test_set_get_paths():
    sorter = Sorter("/input", "/output")
    sorter.set_file_path("/new_input")
    sorter.set_target_path("/new_output")
    assert sorter.get_file_path() == "/new_input"
    assert sorter.get_target_path() == "/new_output"

def test_create_client_directory_same_last_name():
    sorter = Sorter("", "")
    result = sorter.create_client_directory("John Doe", "Jane Doe")
    assert result == "Doe, John & Jane"

def test_create_client_directory_different_last_name():
    sorter = Sorter("", "")
    result = sorter.create_client_directory("John Smith", "Jane Doe")
    assert result == "Smith, John & Doe, Jane"

def test_create_business_directory():
    sorter = Sorter("", "")
    result = sorter.create_business_directory("TEST LLC", "AUX INC")
    assert result == "TEST LLC & AUX INC"

def test_create_client_filename():
    sorter = Sorter("", "")
    row = pd.Series({
        CLIENT_NAME: "John Smith",
        YEAR: "2022",
        DESCRIPTION: "Tax Return"
    })
    assert sorter.create_client_filename(row) == "Smith 2022 Tax Return.pdf"

def test_create_business_filename():
    sorter = Sorter("", "")
    row = pd.Series({
        CLIENT_NAME: "TEST LLC",
        YEAR: "2022",
        DESCRIPTION: "Tax Return"
    })
    assert sorter.create_business_filename(row) == "TEST 2022 Tax Return.pdf"

@patch("os.rename")
@patch("os.makedirs")
@patch("os.path.exists")
def test_sort_files_client(mock_exists, mock_makedirs, mock_rename, sample_data_client):
    sorter = Sorter("/files", "/target")
    sample_data_client = sample_data_client.copy()

    mock_exists.side_effect = lambda path: True

    sorter.sort_files(sample_data_client)

    expected_directory = os.path.join("/target", "Doe, John & Jane", INCOME_TAX)
    expected_dest = os.path.join(expected_directory, "Doe 2023 Form 1040.pdf")
    expected_source = os.path.join("/files", "file1.pdf")

    mock_makedirs.assert_called_once_with(expected_directory, exist_ok=True)
    mock_rename.assert_called_once_with(expected_source.replace("\\", "/"), expected_dest.replace("\\", "/"))

@patch("os.rename")
@patch("os.makedirs")
@patch("os.path.exists")
def test_sort_files_business(mock_exists, mock_makedirs, mock_rename, sample_data_business):
    sorter = Sorter("/files", "/target")
    sample_data_business = sample_data_business.copy()

    mock_exists.side_effect = lambda path: True

    sorter.sort_files(sample_data_business)

    expected_directory = os.path.join("/target", "TEST LLC & AUX INC", INCOME_TAX)
    expected_dest = os.path.join(expected_directory, "TEST 2023 Invoice.pdf")
    expected_source = os.path.join("/files", "biz1.pdf")

    mock_makedirs.assert_called_once_with(expected_directory, exist_ok=True)
    mock_rename.assert_called_once_with(expected_source.replace("\\", "/"), expected_dest.replace("\\", "/"))

@patch("os.path.exists", return_value=False)
def test_sort_files_invalid_paths(mock_exists, sample_data_client):
    sorter = Sorter("/invalid", "/target")
    sorter.sort_files(sample_data_client)

@patch("os.path.exists", side_effect=lambda path: "file1.pdf" not in path)
def test_sort_file_skips_missing_file(mock_exists, sample_data_client):
    sorter = Sorter("/files", "/target")
    sample_data_client = sample_data_client.copy()
    with patch("os.makedirs") as mock_mkdir, patch("os.rename") as mock_rename:
        sorter.sort_files(sample_data_client)
        mock_mkdir.assert_not_called()
        mock_rename.assert_not_called()

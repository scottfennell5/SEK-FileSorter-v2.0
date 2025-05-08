# test_controller.py
import pytest
from unittest.mock import MagicMock, patch

from src.Core.Controller import Controller
from src.Utility.constants import (
    FILE_NAME, STATUS, CLIENT_NAME, CLIENT_2_NAME, CLIENT_TYPE, YEAR, DESCRIPTION,
    FILES_ID, TARGET_ID, CLIENT
)

@pytest.fixture
def controller():
    with patch("src.Core.Controller.DataHandler") as MockDataHandler, \
         patch("src.Core.Controller.Sorter") as MockSorter:
        mock_datahandler = MockDataHandler.return_value
        mock_sorter = MockSorter.return_value
        return Controller(mock_datahandler, mock_sorter)

def test_initialization(controller):
    assert hasattr(controller, "data_handler")
    assert hasattr(controller, "sorter")
    assert controller.observers  # should include dataHandler and sorter

def test_set_observer_filepath(controller):
    observer = MagicMock()
    controller.observers = [observer]
    controller.set_observer_filepath("some/path")
    observer.set_file_path.assert_called_with("some/path")
    observer.update.assert_called_once()

def test_set_observer_targetpath(controller):
    observer = MagicMock()
    controller.observers = [observer]
    controller.set_observer_targetpath("target/path")
    observer.set_target_path.assert_called_with("target/path")
    observer.update.assert_called_once()

def test_get_path_valid(controller):
    controller.data_handler.get_file_path.return_value = "/file"
    controller.data_handler.get_target_path.return_value = "/target"
    controller.data_handler.get_browser_path.return_value = "/browser"
    assert controller.get_path(FILES_ID) == "/file"
    assert controller.get_path(TARGET_ID) == "/target"

def test_get_path_invalid_logs_error(controller, caplog):
    caplog.set_level("ERROR")
    result = controller.get_path("INVALID_ID")
    assert result == ""
    assert "pathID invalid" in caplog.text

def test_set_path_valid(controller):
    controller.set_observer_filepath = MagicMock()
    controller.set_path(FILES_ID, "new/file/path")
    controller.set_observer_filepath.assert_called_with("new/file/path")

def test_set_path_empty_logs_warning(controller, caplog):
    caplog.set_level("WARNING")
    controller.set_path(FILES_ID, "")
    assert "called with empty path" in caplog.text

def test_save_row_changes_valid(controller):
    file_data = {
        FILE_NAME: "file.pdf",
        CLIENT_NAME: "John Doe",
        CLIENT_2_NAME: "",
        CLIENT_TYPE: "individual",
        YEAR: "2024",
        DESCRIPTION: "some description"
    }
    controller.clean_and_validate_row = MagicMock(return_value=(file_data, []))
    controller.data_handler.update_row = MagicMock()
    errors = controller.save_row_changes(file_data, False)
    assert errors == []
    controller.data_handler.update_row.assert_called_once()

def test_clean_and_validate_row_invalid_data():
    ctrl = Controller()
    file_data = {
        FILE_NAME: "badfile.pdf",
        STATUS: True,
        CLIENT_TYPE: CLIENT,
        CLIENT_NAME: "InvalidName##",
        CLIENT_2_NAME: "Another@Name",
        YEAR: "abc",
        DESCRIPTION: "   "
    }
    cleaned, errors = ctrl.clean_and_validate_row(file_data, client2=True)
    assert "Client 1" in errors
    assert "Client 2" in errors
    assert "Year" in errors
    assert "Description" in errors
    assert cleaned[STATUS] == False

def test_clean_and_validate_row_invalid_type():
    ctrl = Controller()
    file_data = {
        FILE_NAME: "badfile.pdf",
        STATUS: True,
        CLIENT_TYPE: "invalid",
        CLIENT_NAME: "Valid Name",
        CLIENT_2_NAME: "invalid name",
        YEAR: "wrong",
        DESCRIPTION: "    "
    }
    cleaned, errors = ctrl.clean_and_validate_row(file_data, client2=True)
    assert errors == ["Client Type"]
    assert cleaned[CLIENT_TYPE] == "invalid"
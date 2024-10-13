import json
from unittest.mock import MagicMock, patch

import pytest

from app.consumer import process_message


def mock_save_location_data(data):
    return True


@pytest.fixture
def mock_connection():
    with patch('kombu.Connection') as mock:
        yield mock


@pytest.fixture
def mock_consumer(mock_connection):
    mock_queue = MagicMock()
    mock_connection.return_value.__enter__.return_value = MagicMock()
    mock_connection.return_value.__enter__.return_value.Consumer.return_value = mock_queue
    yield mock_queue


def test_process_message_success(mock_consumer):
    test_body = json.dumps({"device_id": 1, "latitude": 42.7128, "longitude": -73.0060})

    with patch('app.crud.save_location_data', side_effect=mock_save_location_data):
        message = MagicMock()
        process_message(test_body, message)

    message.ack.assert_called_once()


def test_process_message_failure(mock_consumer):
    test_body = json.dumps({"device_id": 1, "latitude": 42.7128, "longitude": -73.0060})

    with patch('app.crud.save_location_data', side_effect=Exception("DB Error")):
        message = MagicMock()
        process_message(test_body, message)

    message.reject.assert_called_once()

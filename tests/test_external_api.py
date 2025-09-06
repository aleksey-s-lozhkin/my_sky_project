from unittest.mock import Mock, patch

import pytest
import requests
from requests import ConnectionError, RequestException, Timeout

from src.external_api import currency_convert


def test_missing_api():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.return_value = None
        with pytest.raises(ValueError, match='API_KEY not found'):
            currency_convert('USD', 1)


def test_empty_api():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.return_value = ''

        with pytest.raises(ValueError, match='API_KEY not found'):
            currency_convert('USD', 1)


def test_incorrect_currency():
    with pytest.raises(ValueError, match='Currency must be "USD" or "EUR"'):
        currency_convert('BYR', 1)


def test_negative_amount():
    with pytest.raises(ValueError, match='Amount must be more than zero'):
        currency_convert('USD', -1)


def test_zero_amount():
    with pytest.raises(ValueError, match='Amount must be more than zero'):
        currency_convert('USD', 0)


def test_incorrect_type_amount():
    with pytest.raises(TypeError, match='Amount must be float or integer'):
        currency_convert('USD', '100')


def test_success_usd_transaction():
    with (
        patch('src.external_api.requests.request') as mock_request,
        patch('src.external_api.os.getenv') as mock_getenv,
    ):
        mock_getenv.return_value = 'mock_api_key'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'result': 100}
        mock_request.return_value = mock_response
        result = currency_convert('USD', 100)
        assert isinstance(result, float)
        assert result == 100.0


def test_success_eur_transaction():
    with (
        patch('src.external_api.requests.request') as mock_request,
        patch('src.external_api.os.getenv') as mock_getenv,
    ):
        mock_getenv.return_value = 'mock_api_key'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True, 'result': 100}
        mock_request.return_value = mock_response
        result = currency_convert('EUR', 100)
        assert isinstance(result, float)
        assert result == 100.0


def test_http_400_error():
    test_list = [
        (400, 'Error: HTTP Error 400'),
        (401, 'Error: HTTP Error 401'),
        (403, 'Error: HTTP Error 403'),
        (500, 'Error: HTTP Error 500'),
    ]
    for status_code, expected_result in test_list:
        with (
            patch('src.external_api.requests.request') as mock_request,
            patch('src.external_api.os.getenv') as mock_getenv,
        ):
            mock_getenv.return_value = 'mock_api_key'
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_request.return_value = mock_response
            with pytest.raises(RequestException, match=expected_result):
                currency_convert('USD', 100)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.request')
def test_timeout_error(mock_request, mock_getenv):
    mock_getenv.return_value = 'mock_api_key'
    mock_request.side_effect = requests.Timeout
    with pytest.raises(Timeout, match='Error. Timeout'):
        currency_convert('USD', 100)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.request')
def test_connection_error(mock_request, mock_getenv):
    mock_getenv.return_value = 'mock_api_key'
    mock_request.side_effect = requests.ConnectionError
    with pytest.raises(ConnectionError, match='Error. Check internet connection'):
        currency_convert('USD', 100)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.request')
def test_request_exception(mock_request, mock_getenv):
    mock_getenv.return_value = 'mock_api_key'
    mock_request.side_effect = requests.RequestException('Test error')
    with pytest.raises(RequestException, match='Test error'):
        currency_convert('USD', 100)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.request')
def test_key_error(mock_request, mock_getenv):
    mock_getenv.return_value = 'mock_api_key'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'success': True}
    mock_request.return_value = mock_response
    with pytest.raises(ValueError, match='Incorrect data format'):
        currency_convert('USD', 100)


@patch('src.external_api.os.getenv')
@patch('src.external_api.requests.request')
def test_value_error(mock_request, mock_getenv):
    mock_getenv.return_value = 'mock_api_key'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'success': True, 'result': 'one_hundred'}
    mock_request.return_value = mock_response
    with pytest.raises(ValueError, match='Incorrect data format'):
        currency_convert('USD', 100)

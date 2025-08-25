import os.path

import pytest

from src.decorators import log, write_log


@log(filename='')
def wrong_function_console():
    raise ValueError('Something went wrong!')


@log(filename='')
def right_function_console():
    return 'test'


@log(filename='test.log')
def wrong_function_file():
    raise ValueError('Something went wrong!')


@log(filename='test.log')
def right_function_file():
    return 'test'


def test_log_err(capsys):
    with pytest.raises(ValueError, match='Something went wrong!'):
        wrong_function_console()
    captured = capsys.readouterr()
    output = captured.out
    lines = output.strip().split('\n')
    assert len(lines) == 3
    assert 'start "wrong_function_console"' in output
    assert 'stop "wrong_function_console"' in output
    assert '"wrong_function_console" error: Something went wrong!' in output


def test_log_ok(capsys):
    right_function_console()
    captured = capsys.readouterr()
    output = captured.out
    lines = output.strip().split('\n')
    assert len(lines) == 3
    assert 'start "right_function_console"' in output
    assert 'stop "right_function_console"' in output
    assert '"right_function_console" ok' in output


def test_log_file_err():
    if os.path.exists('test.log'):
        os.remove('test.log')

    with pytest.raises(ValueError, match='Something went wrong!'):
        wrong_function_file()

    with open('test.log', 'r', encoding='utf-8') as log_file:
        output = log_file.read()

    assert 'start "wrong_function_file"' in output
    assert 'stop "wrong_function_file"' in output
    assert '"wrong_function_file" error: Something went wrong!' in output

    os.remove('test.log')


def test_log_file_ok():
    if os.path.exists('test.log'):
        os.remove('test.log')

    right_function_file()

    with open('test.log', 'r', encoding='utf-8') as log_file:
        output = log_file.read()

    assert 'start "right_function_file"' in output
    assert 'stop "right_function_file"' in output
    assert '"right_function_file" ok' in output

    os.remove('test.log')


def test_wrong_filenames():
    wrong_names = [
        ('file<name.log', "Недопустимые символы"),
        ('file>name.log', "Недопустимые символы"),
        ('file:name.log', "Недопустимые символы"),
        ('file"name.log', "Недопустимые символы"),
        ('file/name.log', "Недопустимые символы"),
        ('file\\name.log', "Недопустимые символы"),
        ('file|name.log', "Недопустимые символы"),
        ('file?name.log', "Недопустимые символы"),
        ('file*name.log', "Недопустимые символы"),
        ('a' * 256, "Слишком длинное имя"),
    ]

    for filename, expected_error in wrong_names:
        with pytest.raises(ValueError, match=expected_error):
            write_log('', filename)

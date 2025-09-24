from unittest.mock import patch

from src.user_interaction import (
    apply_date_sorting,
    display_results,
    filter_by_description,
    filter_rub_operations,
    load_transactions,
    select_data_source,
    select_filter_status,
)


def test_select_data_source_success(capsys):

    with patch('builtins.input', return_value='1'):
        result = select_data_source()

        assert result == '1'


@patch('src.user_interaction.get_file_by_drag_and_drop')
@patch('src.user_interaction.get_transactions_from_file')
def test_load_transaction(mock_get, mock_drop):

    mock_drop.return_value = 'test.path'
    mock_get.return_value = [{'test': 'test'}]

    result = load_transactions('1')
    assert result == [{'test': 'test'}]


@patch('builtins.input')
def test_select_filter_status(mock_input):

    mock_input.return_value = 'executed'

    result = select_filter_status()

    assert result == 'EXECUTED'


@patch('src.user_interaction.sort_by_date')
@patch('builtins.input')
def test_apply_date_sorting(mock_input, mock_sort):

    test_data = [{'test': 'test'}]
    mock_input.return_value = 'нет'

    result = apply_date_sorting(test_data)
    assert result == [{'test': 'test'}]

    mock_input.side_effect = ['да', 'по возрастанию']
    mock_sort.return_value = [{'111': '222'}]

    result = apply_date_sorting(test_data)
    assert result == [{'111': '222'}]


@patch('builtins.input')
def test_filter_rub_operations(mock_input):

    test_data = [{'test': 'test'}]
    mock_input.return_value = 'нет'

    result = filter_rub_operations(test_data)

    assert result == [{'test': 'test'}]


@patch('src.user_interaction.process_bank_search')
@patch('builtins.input')
def test_filter_by_description(mock_input, mock_process):

    test_data = [{'test': 'test'}]
    mock_input.return_value = 'нет'

    result = filter_by_description(test_data)

    assert result == [{'test': 'test'}]

    mock_input.side_effect = ['да', ' Перевод']
    mock_process.return_value = [{'111': '222'}]

    result = filter_by_description(test_data)

    assert result == [{'111': '222'}]


@patch('src.user_interaction.output_handler_xlsx_csv')
@patch('src.user_interaction.output_handler_json')
def test_display_results(mock_json, mock_other, capsys):

    test_data = [{'test': 'test'}]

    mock_json.return_value = ['01.01.2023', 'Описание JSON', 'Детали', '100', 'USD']
    mock_other.return_value = ['01.01.2023', 'Описание CSV', 'Детали', '200', 'EUR']

    display_results(test_data, '1')
    captured = capsys.readouterr()
    output = captured.out

    assert 'Описание JSON' in output

    display_results(test_data, '2')
    captured = capsys.readouterr()
    output = captured.out

    assert 'Описание CSV' in output

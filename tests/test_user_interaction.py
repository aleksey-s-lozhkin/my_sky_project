# import pytest
# from unittest.mock import patch
#
# from src.user_interaction import (
#     select_data_source,
#     load_transactions,
#     select_filter_status,
#     apply_date_sorting,
#     filter_rub_operations,
#     filter_by_description,
#     display_results,
# )
#
# @pytest.mark.parametrize(
#     'value, expected',
#     [
#         ('executed', 'EXECUTED'),
#         ('Canceled', 'CANCELED'),
#         ('pEndinG', 'PENDING'),
#     ]
# )
#
# def test_select_filter_status(value, expected):
#     assert select_filter_status(value) == expected

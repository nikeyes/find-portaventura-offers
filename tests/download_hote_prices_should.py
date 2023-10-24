from datetime import datetime
import pytest

from src.commands.download_hotel_prices import DownloadPrices


def test_calculate_output_file_name_with_childen():
    date_execution = datetime(2023, 1, 1)
    date_ini = datetime(2023, 1, 3)
    date_end = datetime(2023, 1, 4)
    children = 2
    children_ages = "6,9"
    adults = 3

    dp = DownloadPrices(
        date_execution=date_execution,
        date_ini=date_ini,
        date_end=date_end,
        children=children,
        children_ages=children_ages,
        adults=adults
    )

    assert dp.file_name_hotels == 'hotels_20230101_a3_c2_6_9.json'
   
def test_calculate_output_file_name_with_childrens_none():
    date_execution = datetime(2023, 1, 1)
    date_ini = datetime(2023, 1, 3)
    date_end = datetime(2023, 1, 4)
    adults = 3
    children = 0
    children_ages = None
    

    dp = DownloadPrices(
        date_execution=date_execution,
        date_ini=date_ini,
        date_end=date_end,
        children=children,
        children_ages=children_ages,
        adults=adults
    )

    assert dp.file_name_hotels == 'hotels_20230101_a3.json'


def test_calculate_output_file_name_with_childrens_empty():
    date_execution = datetime(2023, 1, 1)
    date_ini = datetime(2023, 1, 3)
    date_end = datetime(2023, 1, 4)
    adults = 2
    children = 0
    children_ages = ""
    

    dp = DownloadPrices(
        date_execution=date_execution,
        date_ini=date_ini,
        date_end=date_end,
        children=children,
        children_ages=children_ages,
        adults=adults
    )

    assert dp.file_name_hotels == 'hotels_20230101_a2.json'

    # # Test missing date_ini and date_end
    # with pytest.raises(ValueError):
    #     dp = DownloadPrices(None, date_end, children, children_ages, adults, file_sufix)
    # with pytest.raises(ValueError):
    #     dp = DownloadPrices(date_ini, None, children, children_ages, adults, file_sufix)

    # # Test invalid date_ini and date_end
    # with pytest.raises(TypeError):
    #     dp = DownloadPrices(
    #         "2022-01-01", date_end, children, children_ages, adults, file_sufix
    #     )
    # with pytest.raises(TypeError):
    #     dp = DownloadPrices(
    #         date_ini, "2022-01-03", children, children_ages, adults, file_sufix
    #     )

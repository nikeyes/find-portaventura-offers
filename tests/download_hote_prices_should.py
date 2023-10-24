from datetime import datetime
import pytest

from src.commands.download_hotel_prices import DownloadPrices


def test_download_prices():
    date_execution = datetime(2023, 1, 1)
    date_ini = datetime(2023, 1, 3)
    date_end = datetime(2023, 1, 4)
    children = 2
    children_ages = "6,9"
    adults = 3
    file_sufix = "test"

    # Call the constructor
    dp = DownloadPrices(
        date_execution=date_execution,
        date_ini=date_ini,
        date_end=date_end,
        children=children,
        children_ages=children_ages,
        adults=adults,
        file_sufix=file_sufix,
    )

    # Check that the attributes were set correctly
    assert date_execution == datetime(2023, 1, 1)
    assert dp.date_ini == datetime(2023, 1, 3)
    assert dp.date_end == datetime(2023, 1, 4)
    assert dp.children == 2
    assert dp.children_ages == "6,9"
    assert dp.adults == 3
    assert dp.file_sufix == file_sufix
    assert dp.file_name_hotels == 'hotels_20230101_a3_c2_6,9.json'
    assert dp.file_name_tickets == 'tickets_20230101_a3_c2_6,9.json'
   

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

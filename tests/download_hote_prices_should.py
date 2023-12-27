from datetime import datetime
from unittest import TestCase
from assertpy import assert_that

from src.commands.download_hotel_prices import DownloadPrices


class TestDownloadHotelPrices(TestCase):
    def test_calculate_output_file_name_with_childen(self):
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
            adults=adults,
        )

        assert_that(dp.file_name_hotels).is_equal_to('hotels_20230101_a3_c2_6_9.json')

    def test_calculate_output_file_name_with_childrens_none(self):
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
            adults=adults,
        )

        assert_that(dp.file_name_hotels).is_equal_to('hotels_20230101_a3.json')

    def test_calculate_output_file_name_with_childrens_empty(self):
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
            adults=adults,
        )

        assert_that(dp.file_name_hotels).is_equal_to('hotels_20230101_a2.json')

    def test_calculate_output_file_name_with_childrens_empty(self):
        date_execution = datetime(2023, 1, 1)
        date_ini = datetime(2023, 1, 3)
        date_end = datetime(2023, 1, 4)
        adults = 2
        children = 1
        children_ages = "10"

        dp = DownloadPrices(
            date_execution=date_execution,
            date_ini=date_ini,
            date_end=date_end,
            children=children,
            children_ages=children_ages,
            adults=adults,
        )

        assert_that(dp.file_name_hotels).is_equal_to('hotels_20230101_a2_c1_10.json')

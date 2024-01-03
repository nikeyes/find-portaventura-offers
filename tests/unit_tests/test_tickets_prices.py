from unittest import TestCase
from assertpy import assert_that
from src.commands.download_tickets_prices import TicketPrice
from src.domain.occupancy import Occupancy


class TestDownloadTicketPrices(TestCase):
    def test_get_lowest_price(self):
        ticket_prices = [
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
        ]

        occupancy = Occupancy(ticket_prices=ticket_prices)

        lowest_price = occupancy.get_lowest_price()

        assert_that(lowest_price).is_equal_to(40)

    def test_get_higher_price(self):
        ticket_prices = [
            TicketPrice(date="2022-01-01", price=52),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=48),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
        ]

        occupancy = Occupancy(ticket_prices=ticket_prices)

        lowest_price = occupancy.get_higher_price()

        assert_that(lowest_price).is_equal_to(60)

    def test_get_second_lowest_price(self):
        ticket_prices = [
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
        ]

        occupancy = Occupancy(ticket_prices=ticket_prices)

        second_lowest_price = occupancy.get_second_lowest_price()

        assert_that(second_lowest_price).is_equal_to(50)

    def test_get_second_higher_price(self):
        ticket_prices = [
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=52),
        ]

        occupancy = Occupancy(ticket_prices=ticket_prices)

        second_lowest_price = occupancy.get_second_higher_price()

        assert_that(second_lowest_price).is_equal_to(52)

    def test_get_dates_with_occupancy(self):
        ticket_prices = [
            TicketPrice(date="2022-01-01", price=60),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=48),
            TicketPrice(date="2022-01-05", price=40),
            TicketPrice(date="2022-01-06", price=50),
            TicketPrice(date="2022-01-07", price=52),
            TicketPrice(date="2022-01-08", price=48),
        ]

        occupancy = Occupancy(ticket_prices=ticket_prices)
        result = occupancy.get_dates_with_occupancy_low_high()

        expected_result = [
            {'day': '2022-01-01', 'price': 60, "occupation": "high"},
            {'day': '2022-01-02', 'price': 60, "occupation": "high"},
            {'day': '2022-01-03', 'price': 40, "occupation": "low"},
            {'day': '2022-01-04', 'price': 48, "occupation": "low"},
            {'day': '2022-01-05', 'price': 40, "occupation": "low"},
            {'day': '2022-01-07', 'price': 52, "occupation": "high"},
            {'day': '2022-01-08', 'price': 48, "occupation": "low"},
        ]

        self.assertEqual(result, expected_result)
        # The error message of self.assertEquals is much better
        # than that of assertpy for comparing lists or dictionaries,
        # assert_that(result).is_equal_to(expected_result)

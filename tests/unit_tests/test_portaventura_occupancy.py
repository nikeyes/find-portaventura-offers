from unittest import TestCase
from assertpy import assert_that
from src.commands.download_tickets_prices import TicketPrice
from src.domain.occupancy import Occupancy


class TestOccupancy(TestCase):
    def setUp(self):
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
        self.occupancy = Occupancy(ticket_prices=ticket_prices)

    def test_get_occupancy_high_day(self):
        result = self.occupancy.get_occupancy("2022-01-01")
        assert_that(result).is_equal_to("high")

    def test_get_occupancy_second_high_day(self):
        result = self.occupancy.get_occupancy("2022-01-07")
        assert_that(result).is_equal_to("high")

    def test_get_occupancy_low_day(self):
        result = self.occupancy.get_occupancy("2022-01-03")
        assert_that(result).is_equal_to("low")

    def test_get_occupancy_second_low_day(self):
        result = self.occupancy.get_occupancy("2022-01-04")
        assert_that(result).is_equal_to("low")

    def test_get_occupancy_nonexistent_day(self):
        result = self.occupancy.get_occupancy("2022-01-09")
        assert_that(result).is_none()

import unittest
from src.commands.download_tickets_prices import TicketPrice
from src.commands.occupancy import Occupancy

class TestOccupancy(unittest.TestCase):

    def setUp(self):
        ticket_prices = [ 
            TicketPrice(date="2022-01-01", price=60),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=48),
            TicketPrice(date="2022-01-05", price=40),
            TicketPrice(date="2022-01-06", price=50),
            TicketPrice(date="2022-01-07", price=52),
            TicketPrice(date="2022-01-08", price=48)
            ]
        self.occupancy = Occupancy(ticket_prices=ticket_prices)

    def test_get_occupancy_high_day(self):
        result = self.occupancy.get_occupancy("2022-01-01")
        self.assertEqual(result, "high")
    
    def test_get_occupancy_second_high_day(self):
        result = self.occupancy.get_occupancy("2022-01-07")
        self.assertEqual(result, "high")

    def test_get_occupancy_low_day(self):
        result = self.occupancy.get_occupancy("2022-01-03")
        self.assertEqual(result, "low")
    
    def test_get_occupancy_second_low_day(self):
        result = self.occupancy.get_occupancy("2022-01-04")
        self.assertEqual(result, "low")

    def test_get_occupancy_nonexistent_day(self):
        result = self.occupancy.get_occupancy("2022-01-09")
        self.assertIsNone(result)
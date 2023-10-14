import unittest
from src.commands.download_tickets_prices import TicketPrice
from src.commands.portaventura_occupancy import PortaventuraOccupancy

class TestDownloadTicketPrices(unittest.TestCase):

    def test_get_lowest_price(self):
        
        ticket_prices = [ 
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
            ]
        
        portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)
        
        lowest_price = portaventura_occupancy.get_lowest_price()

        self.assertEqual(lowest_price, 40)
    
    def test_get_higher_price(self):

        ticket_prices = [ 
            TicketPrice(date="2022-01-01", price=52),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=48),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
            ]
        
        portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)

        lowest_price = portaventura_occupancy.get_higher_price()

        self.assertEqual(lowest_price, 60)

    def test_get_second_lowest_price(self):
        
        ticket_prices = [ 
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
            ]

        portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)
        
        second_lowest_price = portaventura_occupancy.get_second_lowest_price()

        self.assertEqual(second_lowest_price, 50)
    
    def test_get_second_higher_price(self):
        
        ticket_prices = [ 
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=52),
            ]

        portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)

        second_lowest_price = portaventura_occupancy.get_second_higher_price()

        self.assertEqual(second_lowest_price, 52)


    
    def test_get_dates_with_occupancy(self):
        
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
        
        portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)
        result = portaventura_occupancy.get_dates_with_occupancy_low_high()

        expected_result = [{'day': '2022-01-01', 'price': 60, "occupation":"high"},
                            {'day': '2022-01-02', 'price': 60, "occupation":"high"},
                            {'day': '2022-01-03', 'price': 40, "occupation":"low"},
                            {'day': '2022-01-04', 'price': 48, "occupation":"low"},
                            {'day': '2022-01-05', 'price': 40, "occupation":"low"},
                            {'day': '2022-01-07', 'price': 52, "occupation":"high"},
                            {'day': '2022-01-08', 'price': 48, "occupation":"low"}]

        self.assertEqual(result, expected_result)
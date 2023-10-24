from datetime import datetime
import unittest
from src.commands.download_tickets_prices import TicketPrice
from src.commands.find_offers import FindOffers, HotelOffer, HotelPrice

from unittest.mock import patch, mock_open

from src.commands.occupancy import Occupancy

class TestFindOffers(unittest.TestCase):

    def setUp(self):
        with patch("builtins.open", mock_open(read_data='{}')):
            self.find_offers = FindOffers(
                hotel_prices_file="hotel_prices.json",
                ticket_prices_file="ticket_prices.json",
                date_ini=datetime(2023, 1, 1),
                date_end=datetime(2023, 1, 7),
                max_offers=5
            )

    def test_get_unique_hotel_names(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=100, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=180, rate=150, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=375, rate=300, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=312.5, rate=250, discount=0.2),
            HotelPrice(name="Hotel D", date="2023-01-01", rate_old=500, rate=400, discount=0.2),
        ]
        result = self.find_offers.get_unique_hotel_names()
        self.assertSetEqual(result, {"Hotel A", "Hotel B", "Hotel C", "Hotel D"})

    def test_get_last_date_with_rate_returns_none_if_no_rates(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=None, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=250, rate=None, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=375, rate=None, discount=0.2),
        ]
        result = self.find_offers.get_last_date_with_rate()
        self.assertIsNone(result)

    def test_get_last_date_with_rate_returns_last_date_with_rate(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=None, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-02", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-03", rate_old=375, rate=300, discount=0.2),
            HotelPrice(name="Hotel D", date="2023-01-04", rate_old=500, rate=None, discount=0.2),
            HotelPrice(name="Hotel E", date="2023-01-05", rate_old=625, rate=500, discount=0.2),
        ]
        result = self.find_offers.get_last_date_with_rate()
        self.assertEqual(result, HotelPrice(name="Hotel E", date="2023-01-05", rate_old=625, rate=500, discount=0.2))

    def test_get_minor_rates_only_port_aventura(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=100, discount=0.2),
            HotelPrice(name="Hotel El Paso", date="2023-01-01", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=180, rate=150, discount=0.2),
            HotelPrice(name="Hotel Colorado Creek", date="2023-01-01", rate_old=375, rate=300, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=312.5, rate=250, discount=0.2),
            HotelPrice(name="Hotel Gold River", date="2023-01-01", rate_old=500, rate=400, discount=0.2),
            HotelPrice(name="Hotel D", date="2023-01-01", rate_old=500, rate=400, discount=0.2),
        ]

        self.find_offers.occupancy = Occupancy(ticket_prices=[  
            TicketPrice(date="2023-01-01", price=60),
            TicketPrice(date="2023-01-02", price=60),
            TicketPrice(date="2023-01-03", price=40),
            TicketPrice(date="2023-01-04", price=48),
            TicketPrice(date="2023-01-05", price=40),
            TicketPrice(date="2023-01-06", price=50),
            TicketPrice(date="2023-01-07", price=52),
            TicketPrice(date="2023-01-08", price=48)
            ])
        
        result = self.find_offers.get_minor_rates_only_port_aventura()
        
        expected_result = [
            HotelOffer(name="Hotel El Paso", rate=200, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel Colorado Creek", rate=300, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel Gold River", rate=400, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
        ]
        self.assertEqual(result, expected_result)

    def test_get_minor_rates_only_port_aventura_with_no_port_aventura_hotels(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=100, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=375, rate=300, discount=0.2),
        ]
        result = self.find_offers.get_minor_rates_only_port_aventura()
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_get_minor_rates_only_this_hotel_returns_empty_list_if_no_hotels(self):
        self.find_offers.hotel_prices = []
        result = self.find_offers.get_minor_rates_only_this_hotel("Hotel A")
        self.assertEqual(result, [])

    def test_get_minor_rates_only_this_hotel_returns_empty_list_if_hotel_not_found(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=375, rate=300, discount=0.2),
        ]
        result = self.find_offers.get_minor_rates_only_this_hotel("Hotel A")
        self.assertEqual(result, [])

    def test_get_minor_rates_only_this_hotel_returns_minor_rates_for_hotel(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=100, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=625, rate=50, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-02", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-03", rate_old=375, rate=300, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-04", rate_old=500, rate=400, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-05", rate_old=625, rate=500, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-06", rate_old=625, rate=500, discount=0.2),
            HotelPrice(name="Hotel A", date="2023-01-07", rate_old=625, rate=500, discount=0.2),
            
        ]

        self.find_offers.occupancy = Occupancy(ticket_prices=[  
            TicketPrice(date="2023-01-01", price=60),
            TicketPrice(date="2023-01-02", price=60),
            TicketPrice(date="2023-01-03", price=40),
            TicketPrice(date="2023-01-04", price=48),
            TicketPrice(date="2023-01-05", price=40),
            TicketPrice(date="2023-01-06", price=50),
            TicketPrice(date="2023-01-07", price=52),
            TicketPrice(date="2023-01-08", price=48)
            ])
        
        result = self.find_offers.get_minor_rates_only_this_hotel("Hotel A")

        expected_result = [
            HotelOffer(name="Hotel A", rate=100, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel A", rate=200, date="2023-01-02", occupancy="high", occupancy_next_day="low", day_of_week="Monday"),
            HotelOffer(name="Hotel A", rate=300, date="2023-01-03", occupancy="low", occupancy_next_day="low", day_of_week="Tuesday"),
            HotelOffer(name="Hotel A", rate=400, date="2023-01-04", occupancy="low", occupancy_next_day="low", day_of_week="Wednesday"),
            HotelOffer(name="Hotel A", rate=500, date="2023-01-05", occupancy="low", occupancy_next_day=None, day_of_week="Thursday"),
        ]
        self.assertEqual(result, expected_result)
        

    def test_get_minor_rates_all_hotels_returns_list_of_hotel_offers(self):
        self.find_offers.hotel_prices = [
            HotelPrice(name="Hotel A", date="2023-01-01", rate_old=120, rate=100, discount=0.2),
            HotelPrice(name="Hotel El Paso", date="2023-01-01", rate_old=250, rate=200, discount=0.2),
            HotelPrice(name="Hotel B", date="2023-01-01", rate_old=180, rate=150, discount=0.2),
            HotelPrice(name="Hotel Colorado Creek", date="2023-01-01", rate_old=375, rate=300, discount=0.2),
            HotelPrice(name="Hotel C", date="2023-01-01", rate_old=312.5, rate=250, discount=0.2),
            HotelPrice(name="Hotel Gold River", date="2023-01-01", rate_old=500, rate=400, discount=0.2),
            HotelPrice(name="Hotel D", date="2023-01-01", rate_old=500, rate=450, discount=0.2),
        ]

        self.find_offers.occupancy = Occupancy(ticket_prices=[  
            TicketPrice(date="2023-01-01", price=60),
            TicketPrice(date="2023-01-02", price=60),
            TicketPrice(date="2023-01-03", price=40),
            TicketPrice(date="2023-01-04", price=48),
            TicketPrice(date="2023-01-05", price=40),
            TicketPrice(date="2023-01-06", price=50),
            TicketPrice(date="2023-01-07", price=52),
            TicketPrice(date="2023-01-08", price=48)
            ])

        result = self.find_offers.get_minor_rates_all_hotels()

        expected_result = [
            HotelOffer(name="Hotel A", rate=100, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel B", rate=150, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel El Paso", rate=200, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel C", rate=250, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),
            HotelOffer(name="Hotel Colorado Creek", rate=300, date="2023-01-01", occupancy="high", occupancy_next_day="high", day_of_week="Sunday"),            
        ]

        self.assertEqual(result, expected_result)

    def test_get_minor_rates_all_hotels_returns_empty_list_if_no_hotels(self):
        self.find_offers.hotel_prices = []

        result = self.find_offers.get_minor_rates_all_hotels()

        expected_result = []

        self.assertEqual(result, expected_result)
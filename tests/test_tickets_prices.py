import unittest
from unittest.mock import patch, MagicMock
from src.commands.download_tickets_prices import DownloadTicketPrices
import json

class TestDownloadTicketPrices(unittest.TestCase):

    def setUp(self):
        self.download_ticket_prices = DownloadTicketPrices()

    def test_get_lowest_price(self):
        data = {
            "2022-01-01": {"952719": {"price": 50}},
            "2022-01-02": {"952719": {"price": 60}},
            "2022-01-03": {"952719": {"price": 40}},
            "2022-01-04": {"952719": {"price": 60}},
            "2022-01-05": {"952719": {"price": 40}}
        }

        lowest_price = self.download_ticket_prices.get_lowest_price(data)

        self.assertEqual(lowest_price, 40)
    
    def test_get_higher_price(self):
        data = {
            "2022-01-01": {"952719": {"price": 52}},
            "2022-01-02": {"952719": {"price": 60}},
            "2022-01-03": {"952719": {"price": 48}},
            "2022-01-04": {"952719": {"price": 60}},
            "2022-01-05": {"952719": {"price": 40}}
        }

        lowest_price = self.download_ticket_prices.get_higher_price(data)

        self.assertEqual(lowest_price, 60)

    def test_get_second_lowest_price(self):
        data = {
            "2022-01-01": {"952719": {"price": 50}},
            "2022-01-02": {"952719": {"price": 60}},
            "2022-01-03": {"952719": {"price": 40}},
            "2022-01-04": {"952719": {"price": 60}},
            "2022-01-05": {"952719": {"price": 40}}
        }

        second_lowest_price = self.download_ticket_prices.get_second_lowest_price(data)

        self.assertEqual(second_lowest_price, 50)
    
    def test_get_second_higher_price(self):
        data = {
            "2022-01-01": {"952719": {"price": 50}},
            "2022-01-02": {"952719": {"price": 60}},
            "2022-01-03": {"952719": {"price": 40}},
            "2022-01-04": {"952719": {"price": 60}},
            "2022-01-05": {"952719": {"price": 52}}
        }

        second_lowest_price = self.download_ticket_prices.get_second_higher_price(data)

        self.assertEqual(second_lowest_price, 52)


    @patch('src.commands.download_tickets_prices.DownloadTicketPrices.get_all_tickets_prices')
    def test_get_dates_with_occupancy(self, mock_get_all_tickets_prices):
        mock_response = MagicMock()
        data = {
            "2022-01-01": {"952719": {"price": 60}},
            "2022-01-02": {"952719": {"price": 60}},
            "2022-01-03": {"952719": {"price": 40}},
            "2022-01-04": {"952719": {"price": 48}},
            "2022-01-05": {"952719": {"price": 40}},
            "2022-01-06": {"952719": {"price": 50}},
            "2022-01-07": {"952719": {"price": 52}},
            "2022-01-08": {"952719": {"price": 48}}
        }
        mock_response.text = json.dumps(data)
        mock_get_all_tickets_prices.return_value = mock_response

        download_ticket_prices = DownloadTicketPrices()
        result = download_ticket_prices.get_dates_with_occupancy_low_high()

        expected_result = [{'day': '2022-01-01', 'price': 60, "occupation":"high"},
                            {'day': '2022-01-02', 'price': 60, "occupation":"high"},
                            {'day': '2022-01-03', 'price': 40, "occupation":"low"},
                            {'day': '2022-01-04', 'price': 48, "occupation":"low"},
                            {'day': '2022-01-05', 'price': 40, "occupation":"low"},
                            {'day': '2022-01-07', 'price': 52, "occupation":"high"},
                            {'day': '2022-01-08', 'price': 48, "occupation":"low"}]

        self.assertEqual(result, expected_result)
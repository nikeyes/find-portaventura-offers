from datetime import datetime
import unittest
from unittest.mock import mock_open, patch, MagicMock
from src.commands.download_tickets_prices import DownloadTicketPrices, TicketPrice
import json


class TestDownloadTicketPrices(unittest.TestCase):
    def setUp(self):
        self.download_ticket_prices = DownloadTicketPrices()

    @patch("src.commands.download_tickets_prices.requests.request")
    def test_download(self, mock_request):
        mock_response = MagicMock()
        data = {
            "2022-01-01": {
                "952719": {
                    "price": 50,
                    "discounted": 50,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952720": {
                    "price": 49,
                    "discounted": 49,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952721": {
                    "price": 49,
                    "discounted": 49,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
            },
            "2022-01-02": {
                "952719": {
                    "price": 60,
                    "discounted": 60,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952720": {
                    "price": 46,
                    "discounted": 46,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952721": {
                    "price": 46,
                    "discounted": 46,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
            },
            "2022-01-03": {
                "952719": {
                    "price": 40,
                    "discounted": 40,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952720": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952721": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
            },
            "2022-01-04": {
                "952719": {
                    "price": 60,
                    "discounted": 60,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952720": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952721": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
            },
            "2022-01-05": {
                "952719": {
                    "price": 40,
                    "discounted": 40,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952720": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
                "952721": {
                    "price": 42,
                    "discounted": 42,
                    "banner_ids": None,
                    "alternative_plu": None,
                },
            },
        }
        mock_response.text = json.dumps(data)
        mock_request.return_value = mock_response

        result = self.download_ticket_prices.download()

        expected_result = [
            TicketPrice(date="2022-01-01", price=50),
            TicketPrice(date="2022-01-02", price=60),
            TicketPrice(date="2022-01-03", price=40),
            TicketPrice(date="2022-01-04", price=60),
            TicketPrice(date="2022-01-05", price=40),
        ]

        self.assertEqual(result, expected_result)
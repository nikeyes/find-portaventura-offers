from datetime import datetime
from unittest import TestCase
from src.domain.hotel_rate import HotelRate


class TestHotelRate(TestCase):
    def test_when_set_all_attributes_then_attributes_are_set_correctly(self):
        date = datetime(2022, 1, 1)
        hotel = {"hotelName": "Hotel A", "ratePlan": {"rate": 100.0, "rateOld": 120.0, "discount": 0.2}}

        hr = HotelRate(date, hotel)

        expected_result = {
            "date": "2022-01-01",
            "name": "Hotel A",
            "rate": 100.0,
            "rate_old": 120.0,
            "discount": 0.2,
        }

        self.assertEqual(hr.__dict__, expected_result)

    def test_when_missing_rate_plan_then_it_has_none_values(self):
        hotel = {"hotelName": "Hotel B"}

        date = datetime(2022, 1, 1)
        hr = HotelRate(date, hotel)

        expected_result = {
            "date": "2022-01-01",
            "name": "Hotel B",
            "rate": None,
            "rate_old": None,
            "discount": None,
        }

        self.assertEqual(hr.__dict__, expected_result)

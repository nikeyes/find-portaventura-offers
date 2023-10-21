from datetime import datetime
from assertpy import assert_that
from src.commands.download_hotel_prices import HotelRate

class GivenHotelRate:
    def when_set_all_attributes_then_attributes_are_set_correctly(self):
        date = datetime(2022, 1, 1)
        hotel = {
            "hotelName": "Hotel A",
            "ratePlan": {
                "rate": 100.0,
                "rateOld": 120.0,
                "discount": 0.2
            }
        }

        hr = HotelRate(date, hotel)

        assert_that(hr.date).is_equal_to("2022-01-01")
        assert_that(hr.name).is_equal_to("Hotel A")
        assert_that(hr.rate).is_equal_to(100.0)
        assert_that(hr.rate_old).is_equal_to(120.0)
        assert_that(hr.discount).is_equal_to(0.2)

    def when_missing_rate_plan_then_it_has_none_values(self):
        hotel = {
            "hotelName": "Hotel B"
        }

        date = datetime(2022, 1, 1)
        hr = HotelRate(date, hotel)

        assert_that(hr.date).is_equal_to("2022-01-01")
        assert_that(hr.name).is_equal_to("Hotel B")
        assert_that(hr.rate).is_none()
        assert_that(hr.rate_old).is_none()
        assert_that(hr.discount).is_none()

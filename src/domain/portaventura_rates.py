from datetime import datetime
from dataclasses import dataclass
import json
from domain.hotel_rate import HotelRate


@dataclass
class PortaventuraRates:
    download_date_start: str
    download_date_end: str
    query: dict
    hotels_rate = []
    HOTEL_CARIBE_CODE = 112622
    HOTEL_COLORADO_CREEK_CODE = 112624

    def __init__(self, date_start: datetime, date_end: datetime, children: int, children_ages: str, adults: int) -> None:
        self.download_date_start = date_start.strftime("%Y-%m-%d")
        self.download_date_end = date_end.strftime("%Y-%m-%d")

        children_ages_list = []
        if children_ages and len(children_ages) > 0:
            children_ages_list = [int(age) for age in children_ages.split(',')]

        self.generic_query = {
            "languageCode": "es",
            "startDate": None,
            "endDate": None,
            "children": children,
            "adults": adults,
            "childrenAges": children_ages_list,
            "rooms": 1,
            "maxChildren": children,
            "maxAdults": adults,
            "coupon": "",
            "couponType": "Discount",
            "roomsArray": [{"adults": adults, "children": children, "childrenAges": children_ages_list}],
        }

        self.specific_query = {
            "index": 0,
            "languageCode": "es",
            "startDate": None,
            "endDate": None,
            "hotelCode": None,
            "rooms": [{"adults": adults, "children": children, "childrenAges": children_ages_list}],
            "coupon": "",
            "couponType": "Discount",
        }

    def get_generic_hotels_query(self, start_date: datetime, end_date: datetime):
        self.generic_query["startDate"] = start_date.strftime("%Y-%m-%d")
        self.generic_query["endDate"] = end_date.strftime("%Y-%m-%d")
        return self.generic_query

    def get_specific_hotel_query(self, hotel_code: str, start_date: datetime, end_date: datetime):
        self.specific_query["startDate"] = start_date.strftime("%Y-%m-%d")
        self.specific_query["endDate"] = end_date.strftime("%Y-%m-%d")
        self.specific_query["hotelCode"] = hotel_code
        return self.specific_query

    def add_hotel(self, hotel: HotelRate):
        self.hotels_rate.append(hotel)

    def to_json(self):
        data = self.__dict__.copy()
        hotel_list = [hotel.__dict__ for hotel in self.hotels_rate]
        data["hotels_rate"] = hotel_list
        return json.dumps(data, ensure_ascii=False, indent=4)

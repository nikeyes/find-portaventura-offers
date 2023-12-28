from dataclasses import dataclass
from datetime import datetime


@dataclass
class HotelRate:
    date: str
    name: str
    rate: float
    rate_old: float
    discount: float

    def __init__(self, date: datetime, hotel):
        self.date = date.strftime("%Y-%m-%d")
        if hotel is not None:
            self.name = hotel.get("hotelName")
            rate_plan = hotel.get("ratePlan")
            if rate_plan is not None:
                self.rate = rate_plan.get("rate")
                self.rate_old = rate_plan.get("rateOld")
                self.discount = rate_plan.get("discount")
            else:
                self.rate = None
                self.rate_old = None
                self.discount = None

from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import json
import os
from rich.progress import Progress, BarColumn, SpinnerColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn

@dataclass
class HotelRate:
    date: str
    name: str
    rate: float
    rate_old: float
    discount: float

    @classmethod
    def from_json(cls, date, hotel):
        if hotel is None:
            return cls(
                date=date.strftime("%Y-%m-%d"),
                name=None,
                rate=None,
                rate_old=None,
                discount=None,
            )

        rate_plan = hotel.get("ratePlan")
        if rate_plan is None:
            return cls(
                date=date.strftime("%Y-%m-%d"),
                name=hotel.get("hotelName"),
                rate=None,
                rate_old=None,
                discount=None,
            )

        return cls(
            date=date.strftime("%Y-%m-%d"),
            name=hotel.get("hotelName"),
            rate=rate_plan.get("rate"),
            rate_old=rate_plan.get("rateOld"),
            discount=rate_plan.get("discount"),
        )

@dataclass
class PortaventuraRates:
    download_date_start: str
    download_date_end: str
    query: dict
    hotels_rate = []

    def __init__(self, date_start: datetime, date_end: datetime) -> None:
        self.download_date_start = date_start.strftime("%Y-%m-%d")
        self.download_date_end = date_end.strftime("%Y-%m-%d")
        self.query = {
            "languageCode": "es",
            "startDate": None,
            "endDate": None,
            "children": 2,
            "adults": 3,
            "childrenAges": [6, 10],
            "rooms": 1,
            "maxChildren": 2,
            "maxAdults": 3,
            "coupon": "",
            "couponType": "Discount",
            "roomsArray": [
                {
                    "adults": 3,
                    "children": 2,
                    "childrenAges": [6, 10]
                }
            ]
        }

    def get_query(self, start_date: datetime, end_date: datetime):
        self.query["startDate"] = start_date.strftime("%Y-%m-%d")
        self.query["endDate"] = end_date.strftime("%Y-%m-%d")
        return self.query

    def add_hotel(self, hotel: HotelRate):
        self.hotels_rate.append(hotel)

    def to_json(self):
        data = self.__dict__.copy()
        hotel_list = [hotel.__dict__ for hotel in self.hotels_rate]
        data["hotels_rate"] = hotel_list
        return json.dumps(data, ensure_ascii=False, indent=4)

class DownloadPrices:
    date_ini: datetime
    date_end: datetime
    step: timedelta = timedelta(days=1)

    def __init__(self, date_ini: datetime, date_end: datetime) -> None:
        if not date_ini or not date_end:
            raise ValueError("Both date_ini and date_end are mandatory")
        if not isinstance(date_ini, datetime) or not isinstance(date_end, datetime):
            raise TypeError("date_ini and date_end must be of type datetime")

        self.date_ini = date_ini
        self.date_end = date_end

    def download(self):
        current_date = self.date_ini
        num_days = (self.date_end - self.date_ini).days + 1

        progress_columns = (
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TaskProgressColumn(),
            "Elapsed:",
            TimeElapsedColumn(),
            "Remaining:",
            TimeRemainingColumn(),
        )

        with Progress(*progress_columns, transient=False) as progress:
            analysing_task = progress.add_task(
                f"[cyan]Downloading {num_days} days", start=True, total=num_days
            )

            portaventura_rates = PortaventuraRates(
                date_start=self.date_ini, date_end=self.date_end
            )

            while current_date <= self.date_end:
    
                end_date = current_date + timedelta(days=1)
                payload = json.dumps(
                    portaventura_rates.get_query(start_date=current_date, end_date=end_date)
                )

                response = self.make_request(payload)

                if response.status_code == 200:
                    rates_json = response.json()
                    if "hotels" in rates_json:
                        for hotel_data in rates_json["hotels"]:
                            hotel_rate = HotelRate.from_json(current_date, hotel_data)
                            portaventura_rates.add_hotel(hotel=hotel_rate)

                current_date += self.step
                progress.update(analysing_task, advance=1)

            progress.update(analysing_task, completed=num_days)

        file_path = os.path.join("downloaded_data", f"{datetime.today().strftime('%Y%m%d')}.json")
        with open(file_path, "w") as archivo:
            archivo.write(portaventura_rates.to_json())

    def make_request(self, payload):
        url = "https://book.portaventuraworld.com/funnel/hotels/chain"
        headers = {
            "Content-Type": "application/json"
        }
        return requests.post(url, data=payload, headers=headers)

# if __name__ == "__main__":
#     start_date = datetime(2023, 10, 1)
#     end_date = datetime(2023, 10, 4)
#     downloader = DownloadPrices(start_date, end_date)
#     downloader.download()

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

    def __init__(self, date, hotel):
        self.date = date.strftime("%Y-%m-%d")
        if hotel is not None:
            self.name=hotel.get("hotelName")
            rate_plan = hotel.get("ratePlan")
            if rate_plan is not None:     
                self.rate=rate_plan.get("rate")
                self.rate_old=rate_plan.get("rateOld")
                self.discount=rate_plan.get("discount")
            else:
                self.rate=None
                self.rate_old=None
                self.discount=None
                
@dataclass
class PortaventuraRates:
    download_date_start: str
    download_date_end: str
    query: dict
    hotels_rate = []

    def __init__(self, 
                 date_start: datetime, 
                 date_end: datetime, 
                 children: int,
                 children_ages: str,
                 adults: int) -> None:
        self.download_date_start = date_start.strftime("%Y-%m-%d")
        self.download_date_end = date_end.strftime("%Y-%m-%d")
        
        children_ages_list = []
        if len(children_ages)>0:
            children_ages_list = [int(age) for age in children_ages.split(',')]
        

        self.query = {
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
            "roomsArray": [
                {
                    "adults": adults,
                    "children": children,
                    "childrenAges": children_ages_list
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
    children: int
    children_ages: str
    adults: int
    step: timedelta = timedelta(days=1)

    def __init__(self, date_ini: datetime,
                 date_end: datetime, 
                 children: int,
                 children_ages: str,
                 adults: int) -> None:
        if not date_ini or not date_end:
            raise ValueError("Both date_ini and date_end are mandatory")
        if not isinstance(date_ini, datetime) or not isinstance(date_end, datetime):
            raise TypeError("date_ini and date_end must be of type datetime")

        self.date_ini = date_ini
        self.date_end = date_end
        self.children =  children
        self.children_ages = children_ages
        self.adults = adults

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
                date_start=self.date_ini, 
                date_end=self.date_end,
                children=self.children,
                children_ages=self.children_ages,
                adults=self.adults
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
                            hotel_rate = HotelRate(current_date, hotel_data)
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

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

    def __init__(self, date:datetime, hotel):
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
    HOTEL_CARIBE_CODE = 112622
    HOTEL_COLORADO_CREEK_CODE = 112624

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
            "roomsArray": [
                {
                    "adults": adults,
                    "children": children,
                    "childrenAges": children_ages_list
                }
            ]
        }

        self.specific_query = {
            "index": 0,
            "languageCode": "es",
            "startDate": None,
            "endDate": None,
            "hotelCode": None,
            "rooms": [
                {
                "adults": adults,
                "children": children,
                "childrenAges": children_ages_list
                }
            ],
            "coupon": "",
            "couponType": "Discount"
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

class DownloadPrices:
    date_ini: datetime
    date_end: datetime
    children: int
    children_ages: str
    adults: int
    step: timedelta = timedelta(days=1)
    file_sufix: str = None

    def __init__(self,
                 date_execution: datetime,
                 date_ini: datetime,
                 date_end: datetime, 
                 children: int,
                 children_ages: str,
                 adults: int,
                 file_sufix: str) -> None:
        if not date_ini or not date_end:
            raise ValueError("Both date_ini and date_end are mandatory")
        if not isinstance(date_ini, datetime) or not isinstance(date_end, datetime):
            raise TypeError("date_ini and date_end must be of type datetime")

        self.date_execution = date_execution
        self.date_ini = date_ini
        self.date_end = date_end
        self.children =  children
        self.children_ages = children_ages
        self.adults = adults
        self.file_sufix = file_sufix
        self.file_name_hotels = f"hotels_{self.date_execution.strftime('%Y%m%d')}_a{self.adults}_c{self.children}_{self.children_ages}.json"
        self.file_name_tickets = f"tickets_{self.date_execution.strftime('%Y%m%d')}_a{self.adults}_c{self.children}_{self.children_ages}.json"


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

                response = self.make_generic_hotels_request(portaventura_rates= portaventura_rates, 
                                             start_date=current_date, 
                                             end_date=end_date)

                if response.status_code == 200:
                    rates_json = response.json()
                    if "hotels" in rates_json:
                        for hotel_data in rates_json["hotels"]:
                            if hotel_data["isAvailable"] == True:
                                hotel_rate = HotelRate(current_date, hotel_data)
                                portaventura_rates.add_hotel(hotel=hotel_rate)
                            
                                if hotel_data["hotelCode"] == portaventura_rates.HOTEL_CARIBE_CODE:
                                    hotel_rate = self.get_specific_room_type_rates(hotel_code=hotel_data["hotelCode"],
                                                                                portaventura_rates=portaventura_rates,
                                                                                start_date=current_date,
                                                                                end_date=end_date,
                                                                                hotel_data=hotel_data, 
                                                                                room_type_to_find="Deluxe Superior Club San Juan")
                                    if hotel_rate is not None: portaventura_rates.add_hotel(hotel=hotel_rate)

                                elif hotel_data["hotelCode"] == portaventura_rates.HOTEL_COLORADO_CREEK_CODE:
                                    hotel_rate = self.get_specific_room_type_rates(hotel_code=hotel_data["hotelCode"],
                                                                                portaventura_rates=portaventura_rates,
                                                                                start_date=current_date,
                                                                                end_date=end_date,
                                                                                hotel_data=hotel_data, 
                                                                                room_type_to_find="Deluxe Colorado")
                                    if hotel_rate is not None: portaventura_rates.add_hotel(hotel=hotel_rate)
                                
                current_date += self.step
                progress.update(analysing_task, advance=1)

            progress.update(analysing_task, completed=num_days)

        file_path = os.path.join("downloaded_data", f"hotels_{datetime.today().strftime('%Y%m%d')}_{self.file_sufix}.json")
        with open(file_path, "w") as archivo:
            archivo.write(portaventura_rates.to_json())

        
    def get_specific_room_type_rates(self, hotel_code:str, portaventura_rates, start_date, end_date, hotel_data, room_type_to_find:str):
            if hotel_data["ratePlan"] is not None:
                response = self.make_specific_hotel_request(hotel_code=hotel_code,
                                                            portaventura_rates=portaventura_rates, 
                                                            start_date=start_date, 
                                                            end_date=end_date)
                
                if response.status_code == 200:
                    rates_json = response.json()
                    room_type = self.find_room_type(rates_json, room_type_to_find)
                    hotel_rate = None
                    if len(room_type) > 0:
                        min_rate = min((room['averageRates'][0]['rate'] for room in room_type), default=999999)
                        
                        temp = {
                                "hotelName":room_type[0]["roomTypeName"],
                                "ratePlan":{
                                    "rate": min_rate,
                                    "rateOld": None,
                                    "discount": 0
                                }
                            }
                        hotel_rate = HotelRate(start_date, temp)
                    return hotel_rate    
    
    def make_generic_hotels_request(self, portaventura_rates:PortaventuraRates, start_date:str, end_date: str):
        url = "https://book.portaventuraworld.com/funnel/hotels/chain"
        headers = {
            "Content-Type": "application/json"
        }

        payload = json.dumps(
                    portaventura_rates.get_generic_hotels_query(start_date=start_date, end_date=end_date)
                )
        
        return requests.post(url, data=payload, headers=headers)
    
    def make_specific_hotel_request(self, hotel_code:str, portaventura_rates:PortaventuraRates, start_date:str, end_date: str):
        url = "https://book.portaventuraworld.com/funnel/hotels/rooms"
        headers = {
            "Content-Type": "application/json"
        }

        payload = json.dumps(
                    portaventura_rates.get_specific_hotel_query(hotel_code=hotel_code, start_date=start_date, end_date=end_date)
                )
        
        return requests.post(url, data=payload, headers=headers)

    def find_room_type(self, data, room_type_to_find):
        found_room_types = [room_type for room_type in data['allRoomTypes'] if room_type.get('roomTypeName') == room_type_to_find]
        return found_room_types
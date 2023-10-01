from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import json
from rich.progress import Progress
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

class HotelRate:
    date:str
    name:str
    rate:float
    rateOld:float
    discount:float

    def __init__(self, date:datetime, name:str, rate:float, rateOld:float, discount:float) -> None:
        self.date = date.strftime("%Y-%m-%d")
        self.name = name
        self.rate = rate
        self.rateOld = rateOld
        self.discount = discount

@dataclass
class PortaventuraRates:
    download_date_start:str
    download_date_end:str
    query:dict
    hotels_rate=[]

    def __init__(self, date_start:datetime, date_end:datetime) -> None:
        self.download_date_start = date_start.strftime("%Y-%m-%d")
        self.download_date_end = date_end.strftime("%Y-%m-%d")
        self.query = {
                "languageCode": "es",
                "startDate": None,
                "endDate": None,
                "children": 2,
                "adults": 3,
                "childrenAges": [6,10],
                "rooms": 1,
                "maxChildren": 2,
                "maxAdults": 3,
                "coupon": "",
                "couponType": "Discount",
                "roomsArray": [
                    {
                    "adults": 3,
                    "children": 2,
                    "childrenAges": [6,10]
                    }
                ]
                }
    
    def get_query(self, start_date:datetime, end_date:datetime):
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
    date_ini:datetime
    date_end:datetime
    step:timedelta = timedelta(days=1)

    def __init__(self, date_ini:datetime, date_end:datetime) -> None:
        if date_ini is None:
            raise ValueError("date_ini is mandatory")
    
        if not isinstance(date_ini, datetime):
            raise TypeError("date_ini must be of type datetime")
        
        if date_end is None:
            raise ValueError("date_end is mandatory")
    
        if not isinstance(date_end, datetime):
            raise TypeError("date_end must be of type datetime")
        
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
            
            portaventura_rates = PortaventuraRates(date_start= self.date_ini ,date_end= self.date_end)

            while current_date <= self.date_end:

                reqUrl = "https://book.portaventuraworld.com/funnel/hotels/chain"

                headersList = {
                "Content-Type": "application/json" 
                }

                endDate = current_date+timedelta(days=1)
                payload = json.dumps(
                            portaventura_rates.get_query(start_date=current_date, 
                                                        end_date=endDate)
                                    )

                response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
                
                rates_json = json.loads(response.text)
                
                name=None
                rate=None
                rateOld=None
                discount=None
                for hotel in rates_json["hotels"]:
                    if "hotelName" in hotel:
                        name = hotel["hotelName"]
                    if "ratePlan" in hotel and hotel["ratePlan"] is not None:
                        rate_plan = hotel["ratePlan"]
                        if "rate" in rate_plan:
                            rate = rate_plan["rate"]
                        if "rateOld" in rate_plan:
                            rateOld = rate_plan["rateOld"]
                        if "discount" in rate_plan:
                            discount = rate_plan["discount"]

                    hotel_rate = HotelRate(date=current_date,
                                           name=name,
                                           rate=rate,
                                           rateOld=rateOld,
                                           discount=discount)
                    
                    
                    portaventura_rates.add_hotel(hotel=hotel_rate)

                current_date += self.step

                progress.update(analysing_task, advance=1)

            progress.update(analysing_task, completed=num_days)
            
        
        with open(f'downloaded_data/{datetime.today().strftime("%Y%m%d")}.json', 'w') as archivo:
            archivo.write(portaventura_rates.to_json())


from dataclasses import dataclass
import datetime
import json
from typing import List

from commands.download_tickets_prices import TicketPrice
from commands.occupancy import Occupancy

@dataclass
class HotelPrice:
    date: str
    name: str
    rate: float
    rate_old: float
    discount: float

class FindOffers:
    data :json = None
    date_ini: datetime
    date_end: datetime
    hotel_prices: List[HotelPrice] = []
    occupancy: Occupancy = None


    def __init__(self,
                hotel_prices_file:str,
                ticket_prices_file:str,
                date_ini: datetime,
                date_end: datetime) -> None:
        
        self.date_ini = date_ini
        self.date_end = date_end
        
        with open(hotel_prices_file, 'r') as json_file: 
            data = json.load(json_file)
            self.hotel_prices = [HotelPrice(date=d['date'], 
                                            name=d['name'], 
                                            rate=d['rate'], 
                                            rate_old=d['rate_old'], 
                                            discount=d['discount']) for d in data['hotels_rate']]


        with open(ticket_prices_file, 'r') as f:
            data = json.load(f)
            ticket_prices: List[TicketPrice] = [TicketPrice(date=price['date'], 
                                                            price=price['price']) for price in data]

        self.occupancy = Occupancy(ticket_prices=ticket_prices)
        


    def print_unique_hotel_names(self):
        unic_names = set()

        for hotel_rate in self.hotel_prices:
            unic_names.add(hotel_rate.name)

        print("------------Unique hotel names:---------------")
        for name in unic_names:
            print(name)

    def print_minor_rates_only_port_aventura(self):
        only_this_hotels = ["Hotel El Paso", 
                            "Hotel Colorado Creek",
                            "Hotel Gold River", 
                            "Hotel Mansión de Lucy", 
                            "Hotel PortAventura", 
                            "Hotel Caribe", 
                            "Hotel Roulette",
                            "Deluxe Colorado",
                            "Deluxe Superior Club San Juan"]

        filtered_hotels = [hotel_rate for hotel_rate in self.hotel_prices if hotel_rate.name in only_this_hotels]

        self.minor_rate(filtered_hotels)

    def print_minor_rates_only_this_hotel(self, hotel:str):

        filtered_hotels = [hotel_rate for hotel_rate in self.hotel_prices if hotel_rate.name == hotel]

        self.minor_rate(filtered_hotels)

    
    def print_minor_rates_all_hotels(self):
            self.minor_rate(self.hotel_prices)
    
    def minor_rate(self, hotels):

        if self.date_ini is not None:
            hotels = [hotel for hotel in hotels if hotel.date >= self.date_ini.strftime("%Y-%m-%d")]
        if self.date_end is not None:
            hotels = [hotel for hotel in hotels if hotel.date <= self.date_end.strftime("%Y-%m-%d")]

        ordered_rates = sorted(hotels, key=lambda rate: rate.rate if rate.rate is not None else float('inf'))
        
        five_minor_rates = ordered_rates[:5]

        for hotel_rate in five_minor_rates:
            date_obj = datetime.datetime.strptime(hotel_rate.date, "%Y-%m-%d")
            day_of_week = date_obj.strftime('%A')
            next_day = (date_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            occupancy = self.occupancy.get_occupancy(hotel_rate.date)
            occupancy_next_day = self.occupancy.get_occupancy(next_day)
            print(f"Date: {hotel_rate.date} ({day_of_week})({occupancy})({occupancy_next_day}), Hotel Name: {hotel_rate.name}, Rate: {hotel_rate.rate}")


    def print_last_date_with_rate(self):
        non_null_rates = [hotel for hotel in self.hotel_prices if hotel.rate is not None]
        if non_null_rates:
            result = max(non_null_rates, key=lambda x: x.date)
            print("The last date with a non-null rate is:", result.date, result.name, result.rate)
        else:
            print("No non-null rates were found on any date.")

   
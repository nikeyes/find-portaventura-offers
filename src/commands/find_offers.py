from dataclasses import dataclass
import datetime
import json
from typing import List

from commands.download_tickets_prices import TicketPrice
from commands.portaventura_occupancy import PortaventuraOccupancy

class FindOffers:
    data :json = None
    date_ini: datetime
    date_end: datetime
    hotels_rate = []
    portaventura_occupancy: PortaventuraOccupancy = None


    def __init__(self,
                hotel_prices:str,
                ticket_prices:str,
                date_ini: datetime,
                date_end: datetime) -> None:
        
        self.date_ini = date_ini
        self.date_end = date_end
        
        with open(hotel_prices, 'r') as json_file: 
            self.data = json.load(json_file)
            self.hotels_rate = self.data["hotels_rate"]

        with open(ticket_prices, 'r') as f:
            data = json.load(f)
            ticket_prices: List[TicketPrice] = [TicketPrice(date=price['date'], price=price['price']) for price in data]

        self.portaventura_occupancy = PortaventuraOccupancy(ticket_prices=ticket_prices)
        


    def print_unique_hotel_names(self):
        unic_names = set()

        for hotel_rate in self.hotels_rate:
            unic_names.add(hotel_rate["name"])

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

        filtered_hotels = [hotel_rate for hotel_rate in self.hotels_rate if hotel_rate["name"] in only_this_hotels]

        self.minor_rate(filtered_hotels)

    def print_minor_rates_only_this_hotel(self, hotel:str):

        filtered_hotels = [hotel_rate for hotel_rate in self.hotels_rate if hotel_rate["name"] == hotel]

        self.minor_rate(filtered_hotels)

    
    def print_minor_rates_all_hotels(self):
            self.minor_rate(self.hotels_rate)
    
    def minor_rate(self, hotels):

        if self.date_ini is not None:
            hotels = [hotel for hotel in hotels if hotel["date"] >= self.date_ini.strftime("%Y-%m-%d")]
        if self.date_end is not None:
            hotels = [hotel for hotel in hotels if hotel["date"] <= self.date_end.strftime("%Y-%m-%d")]

        ordered_rates = sorted(hotels, key=lambda rate: rate["rate"] if rate["rate"] is not None else float('inf'))
        
        five_minor_rates = ordered_rates[:5]

        for hotel_rate in five_minor_rates:
            date_obj = datetime.datetime.strptime(hotel_rate['date'], "%Y-%m-%d")
            day_of_week = date_obj.strftime('%A')
            next_day = (date_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            occupancy = self.portaventura_occupancy.get_occupancy(hotel_rate['date'])
            occupancy_next_day = self.portaventura_occupancy.get_occupancy(next_day)
            print(f"Date: {hotel_rate['date']} ({day_of_week})({occupancy})({occupancy_next_day}), Hotel Name: {hotel_rate['name']}, Rate: {hotel_rate['rate']}")


    def print_last_date_with_rate(self):
        non_null_rates = [hotel for hotel in self.hotels_rate if hotel["rate"] is not None]
        if non_null_rates:
            result = max(non_null_rates, key=lambda x: x["date"])
            print("The last date with a non-null rate is:", result["date"], result["name"], result["rate"])
        else:
            print("No non-null rates were found on any date.")

   
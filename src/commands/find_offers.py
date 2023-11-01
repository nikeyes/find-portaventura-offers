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

@dataclass
class HotelOffer:
    name: str
    rate: float
    date: str
    occupancy: str
    occupancy_next_day: str
    day_of_week: str
   

class FindOffers:
    data :json = None
    date_ini: datetime
    date_end: datetime
    hotel_prices: List[HotelPrice] = []
    occupancy: Occupancy = None
    max_offers: int = 0


    def __init__(self,
                hotel_prices_file:str,
                ticket_prices_file:str,
                date_ini: datetime,
                date_end: datetime,
                max_offers: int) -> None:
        
        self.date_ini = date_ini
        self.date_end = date_end
        self.max_offers = max_offers

        self.hotel_prices = self.load_prices(hotel_prices_file)
                
        self.occupancy = self.load_occupancy(ticket_prices_file)

    def load_prices(self, hotel_prices_file):
        with open(hotel_prices_file, 'r') as json_file: 
            data = json.load(json_file)
            if data != {}:
                return [HotelPrice(date=d['date'], 
                                                name=d['name'], 
                                                rate=d['rate'], 
                                                rate_old=d['rate_old'], 
                                                discount=d['discount']) for d in data.get('hotels_rate')]

    def load_occupancy(self, ticket_prices_file) -> Occupancy:
        
        if ticket_prices_file is not None:
            with open(ticket_prices_file, 'r') as f:
                data = json.load(f)
                if data != {}:
                    ticket_prices: List[TicketPrice] = [TicketPrice(date=price['date'], 
                                                                        price=price['price']) for price in data]

                    return Occupancy(ticket_prices=ticket_prices)
        return Occupancy(ticket_prices=[])
        

    def get_unique_hotel_names(self) -> set:
        unic_names = set()

        for hotel_rate in self.hotel_prices:
            unic_names.add(hotel_rate.name)

        return unic_names

    def print_unique_hotel_names(self):
        unic_names = self.get_unique_hotel_names()

        print("------------Unique hotel names:---------------")
        for name in unic_names:
            print(name)


    def get_last_date_with_rate(self) -> HotelPrice:
        non_null_rates = [hotel for hotel in self.hotel_prices if hotel.rate is not None]
        if non_null_rates:
            return max(non_null_rates, key=lambda x: x.date)
        else:
            return None
        
    def print_last_date_with_rate(self):
        last_date = self.get_last_date_with_rate()
        if last_date:
            print("The last date with a non-null rate is:", last_date.date, last_date.name, last_date.rate)
        else:
            print("No non-null rates were found on any date.")

    def get_minor_rates_only_port_aventura(self) -> List[HotelOffer]:
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

        return self.get_minor_rate(filtered_hotels)

    def get_minor_rates_only_this_hotel(self, hotel:str) -> List[HotelOffer]:

        filtered_hotels = [hotel_rate for hotel_rate in self.hotel_prices if hotel_rate.name == hotel]

        return self.get_minor_rate(filtered_hotels)

    
    def get_minor_rates_all_hotels(self) -> List[HotelOffer]:
            return self.get_minor_rate(self.hotel_prices)
    
    def get_minor_rate(self, hotels_prices) -> List[HotelOffer]:

        if self.date_ini is not None:
            hotels_prices = [hotel for hotel in hotels_prices if hotel.date >= self.date_ini.strftime("%Y-%m-%d")]
        if self.date_end is not None:
            hotels_prices = [hotel for hotel in hotels_prices if hotel.date <= self.date_end.strftime("%Y-%m-%d")]

        ordered_rates = sorted(hotels_prices, key=lambda rate: rate.rate if rate.rate is not None else float('inf'))
        
        five_minor_rates = ordered_rates[:self.max_offers]
        
        hotel_offers: List[HotelOffer] = []

        for hotel_rate in five_minor_rates:
            date_obj = datetime.datetime.strptime(hotel_rate.date, "%Y-%m-%d")
            day_of_week = date_obj.strftime('%A')
            next_day = (date_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            occupancy = self.occupancy.get_occupancy(hotel_rate.date)
            occupancy_next_day = self.occupancy.get_occupancy(next_day)
            
            hotel_offer = HotelOffer(name=hotel_rate.name,
                                    rate=hotel_rate.rate,
                                    date=hotel_rate.date,
                                    occupancy=occupancy,
                                    occupancy_next_day=occupancy_next_day,
                                    day_of_week=day_of_week)
            
            hotel_offers.append(hotel_offer)

            # print(f"Date: {hotel_rate.date} ({day_of_week})({occupancy})({occupancy_next_day}), Hotel Name: {hotel_rate.name}, Rate: {hotel_rate.rate}")
            
        return hotel_offers


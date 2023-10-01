from dataclasses import dataclass
import datetime
import json

@dataclass
class Rate:
    date: datetime
    hotel_name: str
    rate: float


class FindOffers:
    data :json = None
    rates = []

    def __init__(self, data_file:str) -> None:
        file_path = data_file

        with open(file_path, 'r') as json_file:
            self.data = json.load(json_file)

        for day, value in self.data.items():
            if value.get("hotels"):
                for hotel in value["hotels"]:
                    price = hotel["ratePlan"]["rate"] if hotel["ratePlan"] else 999999
                    rate = Rate(date=day, hotel_name= hotel["hotelName"], rate=price)
                    self.rates.append(rate)


    def print_unique_hotel_names(self):
        unic_names = set()

        for rate in self.rates:
            unic_names.add(rate.hotel_name)

        print("Unique hotel names:")
        for name in unic_names:
            print(name)

    def print_minor_rates_only_port_aventura(self):
        only_this_hotels = ["Hotel El Paso", "Hotel Colorado Creek","Hotel Gold River", "Hotel Mansión de Lucy", "Hotel PortAventura", "Hotel Caribe", "Hotel Roulette"]

        filtered_hotels = [rate for rate in self.rates if rate.hotel_name in only_this_hotels]

        self.minor_rate(filtered_hotels)

    def print_minor_rates_only_this_hotel(self, hotel:str):

        filtered_hotels = [rate for rate in self.rates if rate.hotel_name == hotel]

        self.minor_rate(filtered_hotels)

    
    def print_minor_rates_all_hotels(self):
            self.minor_rate(self.rates)


    def minor_rate(self, hotels):
        # minor_rate = min(hotels, key=lambda rate: rate.rate)
        # print(minor_rate)

        ordered_rates = sorted(hotels, key=lambda rate: rate.rate)
        
        five_minor_rates = ordered_rates[:5]

        # Imprimir los 5 objetos con las tasas más bajas
        print("-------------Lowest rates:---------------")
        for rate in five_minor_rates:
            print(f"Date: {rate.date}, Hotel Name: {rate.hotel_name}, Rate: {rate.rate}")


    def print_last_date_with_rate(self):
        sorted_dates = sorted(self.data.keys(), reverse=True)

        # Find the last date with a non-null rate
        last_date = None
        for date in sorted_dates:
            if date in self.data and "hotels" in self.data[date]:
                ratePlan = self.data[date]["hotels"][0]["ratePlan"]
                if ratePlan is not None:
                    last_date = date
                    break

        if last_date:
            print("The last date with a non-null rate is:", last_date)
        else:
            print("No non-null rates were found on any date.")

find_offers = FindOffers('./downloaded_data/20230930_datos_3_adult_2_child.json')
find_offers.print_unique_hotel_names()
print("----------------------------------")
find_offers.print_last_date_with_rate()
find_offers.print_minor_rates_all_hotels()
find_offers.print_minor_rates_only_port_aventura()
find_offers.print_minor_rates_only_this_hotel("Hotel Caribe")
find_offers.print_minor_rates_only_this_hotel("Hotel Mansión de Lucy")
find_offers.print_minor_rates_only_this_hotel("Hotel Colorado Creek")
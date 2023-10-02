from dataclasses import dataclass
import datetime
import json

class FindOffers:
    data :json = None
    hotels_rate = []

    def __init__(self, data_file:str) -> None:
        file_path = data_file

        with open(file_path, 'r') as json_file:
            self.data = json.load(json_file)
            self.hotels_rate = self.data["hotels_rate"]

    def print_unique_hotel_names(self):
        unic_names = set()

        for hotel_rate in self.hotels_rate:
            unic_names.add(hotel_rate["name"])

        print("------------Unique hotel names:---------------")
        for name in unic_names:
            print(name)

    def print_minor_rates_only_port_aventura(self):
        only_this_hotels = ["Hotel El Paso", "Hotel Colorado Creek","Hotel Gold River", "Hotel Mansión de Lucy", "Hotel PortAventura", "Hotel Caribe", "Hotel Roulette"]

        filtered_hotels = [hotel_rate for hotel_rate in self.hotels_rate if hotel_rate["name"] in only_this_hotels]

        self.minor_rate(filtered_hotels)

    def print_minor_rates_only_this_hotel(self, hotel:str):

        filtered_hotels = [hotel_rate for hotel_rate in self.hotels_rate if hotel_rate["name"] == hotel]

        self.minor_rate(filtered_hotels)

    
    def print_minor_rates_all_hotels(self):
            self.minor_rate(self.hotels_rate)


    def minor_rate(self, hotels):
        # minor_rate = min(hotels, key=lambda rate: rate.rate)
        # print(minor_rate)

        ordered_rates = sorted(hotels, key=lambda rate: rate["rate"] if rate["rate"] is not None else float('inf'))
        
        five_minor_rates = ordered_rates[:5]

        # Imprimir los 5 objetos con las tasas más bajas
        print("-------------Lowest rates:---------------")
        for hotel_rate in five_minor_rates:
            print(f"Date: {hotel_rate['date']}, Hotel Name: {hotel_rate['name']}, Rate: {hotel_rate['rate']}")


    def print_last_date_with_rate(self):
        result = max(
            (hotel for hotel in self.hotels_rate if hotel["rate"] is not None),
            key=lambda x: x["date"]
            )

        if result:
            print("The last date with a non-null rate is:",  result["date"], result["name"], result["rate"])
        else:
            print("No non-null rates were found on any date.")

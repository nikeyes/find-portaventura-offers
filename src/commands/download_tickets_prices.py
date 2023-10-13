import requests
import json

class DownloadTicketPrices:
    def __init__(self) -> None:
        pass

    def get_all_tickets_prices(self):
        reqUrl = "https://book.portaventuraworld.com/funnel/tickets/calendar/es?language=es&ids=83"

        headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        return response

    def get_lowest_price(self, data):
        prices = []
        for day in data:
            if "952719" in data[day]:
                prices.append(data[day]["952719"]["price"])

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[0]
    
    def get_higher_price(self, data):
        prices = []
        for day in data:
            if "952719" in data[day]:
                prices.append(data[day]["952719"]["price"])

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[-1]

    
    def get_second_lowest_price(self, data):
        prices = []
        for day in data:
            if "952719" in data[day]:
                prices.append(data[day]["952719"]["price"])

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[1]
    

    def get_second_higher_price(self, data):
        prices = []
        for day in data:
            if "952719" in data[day]:
                prices.append(data[day]["952719"]["price"])

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[-2]
    
    
    def get_dates_with_occupancy_low_high(self):
        
        response = self.get_all_tickets_prices()

        data = json.loads(response.text)

        lowest_price = self.get_lowest_price(data)
        second_lowest_price = self.get_second_lowest_price(data)

        higher_price = self.get_higher_price(data)
        second_higher_price = self.get_second_higher_price(data)
        
        price_days = []

        for day in data:
            if "952719" in data[day]:
                price = data[day]["952719"]["price"]
                if price == lowest_price or price == second_lowest_price:
                    price_days.append({"day":day,"price":price, "occupation":"low"})
                if price == higher_price or price == second_higher_price:
                    price_days.append({"day":day,"price":price, "occupation":"high"})

        return price_days



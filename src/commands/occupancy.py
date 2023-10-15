from typing import List

from commands.download_tickets_prices import TicketPrice


class Occupancy:
    ticket_prices: List[TicketPrice]
    days_occupancy_low_high: List[dict] = []

    def __init__(self, ticket_prices: List[TicketPrice]) -> None:
        self.ticket_prices = ticket_prices
        self.days_occupancy_low_high = self.get_dates_with_occupancy_low_high()


    def get_dates_with_occupancy_low_high(self):
        
        lowest_price = self.get_lowest_price()
        second_lowest_price = self.get_second_lowest_price()

        higher_price = self.get_higher_price()
        second_higher_price = self.get_second_higher_price()
        
        price_days = []

        for tp in self.ticket_prices:
            price = tp.price
            if price == lowest_price or price == second_lowest_price:
                price_days.append({"day":tp.date,"price":tp.price, "occupation":"low"})
            if price == higher_price or price == second_higher_price:
                price_days.append({"day":tp.date,"price":tp.price, "occupation":"high"})

        return price_days

    def get_occupancy(self, day:str) -> str:
        for occupancy in self.days_occupancy_low_high:
            if occupancy["day"] == day:
                return occupancy["occupation"]
    
    def get_lowest_price(self):
        prices = []
        for tp in self.ticket_prices:
            prices.append(tp.price)

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[0]


    def get_higher_price(self):
        prices = []
        for tp in self.ticket_prices:
            prices.append(tp.price)

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[-1]

    
    def get_second_lowest_price(self):
        prices = []
        for tp in self.ticket_prices:
            prices.append(tp.price)

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[1]
    
    def get_second_higher_price(self):
        prices = []
        for tp in self.ticket_prices:
            prices.append(tp.price)

        sorted_prices = sorted(list(set(prices)))
        
        return sorted_prices[-2]



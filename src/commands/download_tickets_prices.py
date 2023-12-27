from dataclasses import dataclass
from datetime import datetime
import os
from typing import List
import requests
import json


@dataclass
class TicketPrice:
    date: str
    price: int


class DownloadTicketPrices:
    def __init__(self) -> None:
        pass

    def download_and_save_to_file(self):
        ticket_prices = self.download()

        file_path = os.path.join("downloaded_data", f"tickets_{datetime.today().strftime('%Y%m%d')}.json")
        with open(file_path, "w") as archivo:
            archivo.write(json.dumps([price.__dict__ for price in ticket_prices], indent=4))

    def download(self) -> List[TicketPrice]:
        reqUrl = "https://book.portaventuraworld.com/funnel/tickets/calendar/es?language=es&ids=83"

        headersList = {"Accept": "*/*", "User-Agent": "Thunder Client (https://www.thunderclient.com)"}

        payload = ""

        response = requests.request("GET", reqUrl, data=payload, headers=headersList)

        data = json.loads(response.text)

        ticket_prices: List[TicketPrice] = []
        for date, prices in data.items():
            if '952719' in prices:
                ticket_prices.append(TicketPrice(date=date, price=prices['952719']['price']))

        return ticket_prices

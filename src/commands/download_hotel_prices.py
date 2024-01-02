import json
import os
from datetime import datetime, timedelta
from typing import List
import requests
from rich.progress import Progress, BarColumn, SpinnerColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn

from domain.hotel_rate import HotelRate
from domain.portaventura_rates import PortaventuraRates


class DownloadPrices:
    date_ini: datetime
    date_end: datetime
    children: int
    children_ages: str
    adults: int
    step: timedelta = timedelta(days=1)
    file_sufix: str = None

    def __init__(
        self, date_execution: datetime, date_ini: datetime, date_end: datetime, children: int, children_ages: str, adults: int
    ) -> None:
        if not date_ini or not date_end:
            raise ValueError("Both date_ini and date_end are mandatory")
        if not isinstance(date_ini, datetime) or not isinstance(date_end, datetime):
            raise TypeError("date_ini and date_end must be of type datetime")

        self.date_execution = date_execution
        self.date_ini = date_ini
        self.date_end = date_end
        self.children = children
        self.children_ages = children_ages
        self.adults = adults
        self.file_name_hotels = self.get_file_name()

    def download(self) -> PortaventuraRates:
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
            analysing_task = progress.add_task(f"[cyan]Downloading {num_days} days", start=True, total=num_days)

            portaventura_rates = PortaventuraRates(
                date_start=self.date_ini,
                date_end=self.date_end,
                children=self.children,
                children_ages=self.children_ages,
                adults=self.adults,
            )

            while current_date <= self.date_end:
                end_date = current_date + timedelta(days=1)

                self.get_prices_standard_rooms(current_date, portaventura_rates, end_date)

                self.get_prices_special_rooms(current_date, portaventura_rates, end_date)

                current_date += self.step
                progress.update(analysing_task, advance=1)

            progress.update(analysing_task, completed=num_days)

        return portaventura_rates

    def download_and_save_to_file(self) -> None:
        portaventura_prices = self.download()
        self.save_hotels_prices(portaventura_prices)

    def save_hotels_prices(self, portaventura_rates) -> None:
        file_path = os.path.join("downloaded_data", self.file_name_hotels)
        with open(file_path, "w", encoding="utf-8") as archivo:
            archivo.write(portaventura_rates.to_json())

    def get_prices_standard_rooms(self, current_date, portaventura_rates, end_date):
        response = self.make_generic_hotels_request(portaventura_rates=portaventura_rates, start_date=current_date, end_date=end_date)

        if response.status_code == 200:
            rates_json = response.json()
            if "hotels" in rates_json:
                for hotel_data in rates_json["hotels"]:
                    if hotel_data["isAvailable"] is True:
                        hotel_rate = HotelRate(current_date, hotel_data)
                        portaventura_rates.add_hotel(hotel=hotel_rate)

    def get_prices_special_rooms(self, current_date, portaventura_rates, end_date):
        self.get_prices_club_san_juan_rooms(current_date, portaventura_rates, end_date)
        self.get_prices_deluxe_colorado_creek_rooms(current_date, portaventura_rates, end_date)

    def get_prices_club_san_juan_rooms(self, current_date, portaventura_rates, end_date):
        hotel_rate = self.get_specific_room_type_rates(
            hotel_code=portaventura_rates.HOTEL_CARIBE_CODE,
            portaventura_rates=portaventura_rates,
            start_date=current_date,
            end_date=end_date,
            room_type_to_find="Deluxe Superior Club San Juan",
        )
        if hotel_rate is not None:
            portaventura_rates.add_hotel(hotel=hotel_rate)

    def get_prices_deluxe_colorado_creek_rooms(self, current_date, portaventura_rates, end_date):
        hotel_rate = self.get_specific_room_type_rates(
            hotel_code=portaventura_rates.HOTEL_COLORADO_CREEK_CODE,
            portaventura_rates=portaventura_rates,
            start_date=current_date,
            end_date=end_date,
            room_type_to_find="Deluxe Colorado",
        )
        if hotel_rate is not None:
            portaventura_rates.add_hotel(hotel=hotel_rate)

    def get_file_name(self):
        if self.children_ages is None or len(self.children_ages) == 0:
            return f"hotels_{self.date_execution.strftime('%Y%m%d')}_a{self.adults}.json"
        return (
            f"hotels_{self.date_execution.strftime('%Y%m%d')}_a{self.adults}_c{self.children}_{self.children_ages.replace(',', '_')}.json"
        )

    def get_specific_room_type_rates(self, hotel_code: str, portaventura_rates, start_date, end_date, room_type_to_find: str):
        response = self.make_specific_hotel_request(
            hotel_code=hotel_code, portaventura_rates=portaventura_rates, start_date=start_date, end_date=end_date
        )

        if response.status_code == 200:
            rates_json = response.json()
            room_type = self.find_room_type(rates_json, room_type_to_find)
            hotel_rate = None
            if len(room_type) > 0:
                min_rate = min((room['averageRates'][0]['rate'] for room in room_type), default=999999)

                temp = {"hotelName": room_type[0]["roomTypeName"], "ratePlan": {"rate": min_rate, "rateOld": None, "discount": 0}}
                hotel_rate = HotelRate(start_date, temp)
            return hotel_rate

    def make_generic_hotels_request(self, portaventura_rates: PortaventuraRates, start_date: str, end_date: str):
        url = "https://book.portaventuraworld.com/funnel/hotels/chain"
        headers = {"Content-Type": "application/json"}

        payload = json.dumps(portaventura_rates.get_generic_hotels_query(start_date=start_date, end_date=end_date))

        return requests.post(url, data=payload, headers=headers, timeout=10)

    def make_specific_hotel_request(self, hotel_code: str, portaventura_rates: PortaventuraRates, start_date: str, end_date: str):
        url = "https://book.portaventuraworld.com/funnel/hotels/rooms"
        headers = {"Content-Type": "application/json"}

        payload = json.dumps(portaventura_rates.get_specific_hotel_query(hotel_code=hotel_code, start_date=start_date, end_date=end_date))

        return requests.post(url, data=payload, headers=headers, timeout=10)

    def find_room_type(self, data, room_type_to_find):
        found_room_types = [room_type for room_type in data['allRoomTypes'] if room_type.get('roomTypeName') == room_type_to_find]
        return found_room_types

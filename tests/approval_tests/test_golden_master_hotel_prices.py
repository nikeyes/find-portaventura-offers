from datetime import datetime
from unittest import TestCase
import json
from mockito import when, unstub, contains
import requests

from approvaltests.approvals import verify
from approvaltests import set_default_reporter

from src.commands.download_hotel_prices import DownloadPrices
from src.domain.portaventura_rates import PortaventuraRates


class TestGoldenMasterDownloadTicketPrices(TestCase):
    def setUp(self) -> None:
        super().setUp()
        set_default_reporter(None)

    def tearDown(self) -> None:
        unstub()
        return super().tearDown()

    def test_download(self):
        when(requests).post(
            'https://book.portaventuraworld.com/funnel/hotels/chain',
            data=any,
            headers=any,
            timeout=any,
        ).thenReturn(MockResponseHotelPrices())
        when(requests).post(
            'https://book.portaventuraworld.com/funnel/hotels/rooms',
            data=contains(f'"hotelCode": {PortaventuraRates.HOTEL_COLORADO_CREEK_CODE}'),
            headers=any,
            timeout=any,
        ).thenReturn(MockResponseDeluxeColoradoPrices())
        when(requests).post(
            'https://book.portaventuraworld.com/funnel/hotels/rooms',
            data=contains(f'"hotelCode": {PortaventuraRates.HOTEL_CARIBE_CODE}'),
            headers=any,
            timeout=any,
        ).thenReturn(MockResponseClubSanJuanPrices())

        download_prices = DownloadPrices(
            date_execution=datetime(2023, 12, 20),
            date_ini=datetime(2023, 12, 31),
            date_end=datetime(2024, 1, 1),
            children=2,
            children_ages="6,10",
            adults=2,
        )
        portaventura_prices = download_prices.download()
        # response = requests.request('POST', 'http://example.com')

        # assert response.status_code == 200
        verify(portaventura_prices.to_json())


class MockResponseHotelPrices:
    def __init__(self):
        self.status_code = 200

    def json(self):
        with open('tests/approval_tests/data_for_tests/data_hotel_prices_1_day.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data


class MockResponseDeluxeColoradoPrices:
    def __init__(self):
        self.status_code = 200

    def json(self):
        with open('tests/approval_tests/data_for_tests/data_rooms_deluxe_colorado_1_day.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data


class MockResponseClubSanJuanPrices:
    def __init__(self):
        self.status_code = 200

    def json(self):
        with open('tests/approval_tests/data_for_tests/data_rooms_club_sanjuan_1_day.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

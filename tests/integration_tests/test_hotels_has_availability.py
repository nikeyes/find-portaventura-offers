import json
from datetime import datetime
from unittest import TestCase

import pytest
import requests
from approvaltests import set_default_reporter
from approvaltests.approvals import verify
from mockito import contains, unstub, when

from src.commands.download_hotel_prices import DownloadPrices
from src.domain.portaventura_rates import PortaventuraRates


@pytest.mark.integration_tests
class TestHotelsHasAvailability(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Código que debe ejecutarse una sola vez para toda la clase
        # Por ejemplo, configuración de conexiones, datos compartidos, etc.
        cls.download_prices = DownloadPrices(
            date_execution=datetime.now(),
            date_ini=datetime(2025, 8, 16),
            date_end=datetime(2025, 8, 17),
            children=2,
            children_ages="8,11",
            adults=2,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        # Limpieza después de todos los tests
        return super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()
        # Código que debe ejecutarse antes de cada test

    def tearDown(self) -> None:
        # Limpieza después de cada test
        return super().tearDown()

    def test_download_mansion_de_lucy(self):
        
        portaventura_prices = self.download_prices.download()
        lucy_rates = [hotel for hotel in portaventura_prices.hotels_rate if "Hotel Mansión de Lucy" in hotel.name]

        assert len(lucy_rates) > 0

    def test_all_hotels_have_availability(self):
        portaventura_prices = self.download_prices.download()
        
        hotels_to_test = [
            "Hotel Mansión de Lucy",
            "Hotel Roulette",
            "Hotel Caribe",
            "Hotel Gold River",
            "Hotel El Paso",
            "Hotel Colorado Creek",
            "Hotel PortAventura",
            "Deluxe Superior Club San Juan",
            "Deluxe Colorado"
        ]
        
        for hotel_name in hotels_to_test:
            hotel_rates = [hotel for hotel in portaventura_prices.hotels_rate if hotel_name in hotel.name]
            assert len(hotel_rates) > 0, f"{hotel_name} debería estar disponible"


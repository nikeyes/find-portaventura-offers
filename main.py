from download_prices import DownloadPrices
from datetime import datetime

from find_offers import FindOffers

date_ini:datetime = datetime(2023, 10, 2)
date_end:datetime = datetime(2023, 10, 5)

dp = DownloadPrices(date_ini=date_ini, date_end=date_end)
dp.download()

find_offers = FindOffers('./downloaded_data/20231002.json')
find_offers.print_unique_hotel_names()
print("----------------------------------")
find_offers.print_last_date_with_rate()
find_offers.print_minor_rates_all_hotels()
find_offers.print_minor_rates_only_port_aventura()
find_offers.print_minor_rates_only_this_hotel("Hotel Caribe")
find_offers.print_minor_rates_only_this_hotel("Hotel Mansión de Lucy")
find_offers.print_minor_rates_only_this_hotel("Hotel Colorado Creek")
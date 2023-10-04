import click
from datetime import datetime
from commands.download_prices import DownloadPrices
from commands.find_offers import FindOffers

@click.group()
def cli():
    pass

@cli.command()
@click.option('--date-ini', type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date in YYYY-MM-DD format')
@click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]), help='End date in YYYY-MM-DD format')
@click.option('--children', default=2, type=int, help='Number of children')
@click.option('--children-ages', default="6,9", type=str, help='Ages of children (comma-separated)')
@click.option('--adults', default=2, type=int, help='Number of adults')
def download_rates(date_ini: datetime, 
                   date_end: datetime, 
                   children: int,
                   children_ages: str,
                   adults: int): 
    dp = DownloadPrices(date_ini=date_ini, 
                        date_end=date_end,
                        children = children,
                        children_ages=children_ages,
                        adults=adults)
    dp.download()
    click.echo("Rates downloaded successfully.")

@cli.command()
@click.option('--data-path', type=click.Path(exists=True), help='Path to the data file')
def find_offers(data_path):
    find_offers_instance = FindOffers(data_path)
    find_offers_instance.print_unique_hotel_names()
    click.echo("----------------------------------")
    find_offers_instance.print_last_date_with_rate()
    find_offers_instance.print_minor_rates_all_hotels()
    find_offers_instance.print_minor_rates_only_port_aventura()
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Caribe")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Mansión de Lucy")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Colorado Creek")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Gold River")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel PortAventura")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel El Paso")
    find_offers_instance.print_minor_rates_only_this_hotel("Deluxe Superior Club San Juan")
    


if __name__ == '__main__':
    cli()

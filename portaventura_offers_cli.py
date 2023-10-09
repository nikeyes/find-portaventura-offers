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
@click.option('--file-sufix', default="", type=str, help='Export filename sufix')
def download_rates(date_ini: datetime, 
                   date_end: datetime, 
                   children: int,
                   children_ages: str,
                   adults: int,
                   file_sufix: str): 
    dp = DownloadPrices(date_ini=date_ini, 
                        date_end=date_end,
                        children = children,
                        children_ages=children_ages,
                        adults=adults,
                        file_sufix=file_sufix)
    dp.download()
    click.echo("Rates downloaded successfully.")

@cli.command()
@click.option('--data-path', type=click.Path(exists=True), help='Path to the data file')
@click.option('--date-ini', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date in YYYY-MM-DD format')
@click.option('--date-end', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='End date in YYYY-MM-DD format')
def find_offers(data_path:str, date_ini:datetime, date_end:datetime):
    find_offers_instance = FindOffers(data_file=data_path,
                                      date_ini=date_ini, 
                                      date_end=date_end)


    find_offers_instance.print_unique_hotel_names()
    click.echo("----------------------------------")
    find_offers_instance.print_last_date_with_rate()
    print("-------------Lowest rates all hotels:---------------")
    find_offers_instance.print_minor_rates_all_hotels()
    print("-------------Lowest rates only Portaventura hotels:---------------")
    find_offers_instance.print_minor_rates_only_port_aventura()
    print("-------------Lowest rates Caribe:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Caribe")
    print("-------------Lowest rates Deluxe Superior Club San Juan:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Deluxe Superior Club San Juan")
    print("-------------Lowest rates Mansión de Lucy:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Mansión de Lucy")
    print("-------------Lowest rates Colorado Creek:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Colorado Creek")
    print("-------------Lowest rates Deluxe Colorado:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Deluxe Colorado")
    print("-------------Lowest rates Gold River:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel Gold River")
    print("-------------Lowest rates PortAventura:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel PortAventura")
    print("-------------Lowest rates El Paso:---------------")
    find_offers_instance.print_minor_rates_only_this_hotel("Hotel El Paso")


    
    


if __name__ == '__main__':
    cli()

import click
from datetime import datetime
from commands.download_hotel_prices import DownloadPrices
from commands.find_offers import FindOffers
from commands.download_tickets_prices import DownloadTicketPrices

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
    
    dtp = DownloadTicketPrices()
    dtp.download_and_save_to_file()

    dp = DownloadPrices(date_ini=date_ini, 
                        date_end=date_end,
                        children = children,
                        children_ages=children_ages,
                        adults=adults,
                        file_sufix=file_sufix)
    dp.download()
    click.echo("Rates downloaded successfully.")


@cli.command()
def download_ticket_prices():
    dtp = DownloadTicketPrices()
    dtp.download()


@cli.command()
@click.option('--hotel-prices', type=click.Path(exists=True), help='Path to the hotel prices file')
@click.option('--ticket-prices', type=click.Path(exists=True), help='Path to the ticket prices file')
@click.option('--date-ini', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date in YYYY-MM-DD format')
@click.option('--date-end', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='End date in YYYY-MM-DD format')
def find_offers(hotel_prices:str, 
                ticket_prices:str, 
                date_ini:datetime, 
                date_end:datetime):
    find_offers_instance = FindOffers(hotel_prices=hotel_prices,
                                      ticket_prices=ticket_prices,
                                      date_ini=date_ini, 
                                      date_end=date_end)


    from pprint import pprint

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



# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from google.oauth2.credentials import Credentials
# @cli.command()
# def send_email():
    
#     # Configura las credenciales OAuth obtenidas de la Consola de Desarrolladores de Google
#     credentials = Credentials.from_authorized_user_info({
#         'client_id': 'TU_CLIENT_ID',
#         'client_secret': 'TU_CLIENT_SECRET',
#         'token': 'TU_TOKEN_DE_ACCESO'
#     })

#     # Configura la información del correo
#     sender_email = 'tucorreo@gmail.com'
#     receiver_email = 'destinatario@example.com'
#     subject = 'Asunto del correo'
#     message = 'Cuerpo del correo'

#     # Crea el mensaje
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(message, 'plain'))

#     try:
#         # Conéctate al servidor SMTP de Gmail
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()

#         # Inicia sesión con las credenciales OAuth
#         server.login(sender_email, credentials)

#         # Envía el correo
#         server.sendmail(sender_email, receiver_email, msg.as_string())
#         print('El correo se ha enviado con éxito.')

#     except Exception as e:
#         print(f'Error al enviar el correo: {str(e)}')

#     finally:
#         server.quit()

    
    


if __name__ == '__main__':
    cli()

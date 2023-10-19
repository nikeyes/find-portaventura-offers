import unittest
from unittest.mock import patch, MagicMock
from typing import List
from src.commands.find_offers import HotelOffer
from src.main import send_offers_by_email

class TestSendOffersByMail(unittest.TestCase):
    @patch('src.main.send_offers_by_email.send_mail')
    def test_send_offers_by_mail(self, mock_send_mail):
        # Create a list of HotelOffer objects to send
        offers = [
            HotelOffer(name='Hotel A', price=100),
            HotelOffer(name='Hotel B', price=200),
            HotelOffer(name='Hotel C', price=300),
        ]
        
        # Call the function to send the offers by email
        send_offers_by_email(offers)
        
        # Check that the email was sent with the correct arguments
        mock_send_mail.assert_called_once_with(
            subject='New hotel offers',
            body='Here are the latest hotel offers:\n\n'
                 'Hotel A - $100\n'
                 'Hotel B - $200\n'
                 'Hotel C - $300\n',
            to='jorge@example.com'
        )


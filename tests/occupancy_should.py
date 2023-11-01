from src.commands.download_tickets_prices import TicketPrice
from src.commands.occupancy import Occupancy
from assertpy import assert_that



class TestOccupancy:
    def setup(self):
        
        self.ticket_prices = [
            TicketPrice("2022-01-01", 100.0),
            TicketPrice("2022-01-02", 200.0),
            TicketPrice("2022-01-03", 300.0),
            TicketPrice("2022-01-04", 400.0),
            TicketPrice("2022-01-05", 500.0),
            TicketPrice("2022-01-06", 600.0),
        ]

    def test_get_dates_with_occupancy_low(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        days = oc.get_dates_with_occupancy_low_high()
        
        assert_that(days).is_length(4)
        
        assert_that(days[0]["day"]).is_equal_to("2022-01-01")
        assert_that(days[0]["price"]).is_equal_to(100.0)
        assert_that(days[0]["occupation"]).is_equal_to("low")

        assert_that(days[1]["day"]).is_equal_to("2022-01-02")
        assert_that(days[1]["price"]).is_equal_to(200.0)
        assert_that(days[1]["occupation"]).is_equal_to("low")
    
    def test_get_dates_with_occupancy_high(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        days = oc.get_dates_with_occupancy_low_high()
        
        assert_that(days).is_length(4)
        
        assert_that(days[2]["day"]).is_equal_to("2022-01-05")
        assert_that(days[2]["price"]).is_equal_to(500.0)
        assert_that(days[2]["occupation"]).is_equal_to("high")

        assert_that(days[3]["day"]).is_equal_to("2022-01-06")
        assert_that(days[3]["price"]).is_equal_to(600.0)
        assert_that(days[3]["occupation"]).is_equal_to("high")

    def test_get_dates_without_occupancy(self):
        
        oc = Occupancy(ticket_prices=[])

        days = oc.get_dates_with_occupancy_low_high()
        
        assert_that(days).is_length(0)

    def test_get_occupancy_without_prices(self):
        # Test get_dates_with_occupancy_low_high
        oc = Occupancy(ticket_prices=[])

        occupancy = oc.get_occupancy("2022-01-01")
        
        assert_that(occupancy).is_none()


    def test_get_occupancy_high(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        occupancy_high_1 = oc.get_occupancy("2022-01-05")
      
        occupancy_high_2 = oc.get_occupancy("2022-01-06")
        
        assert_that(occupancy_high_1).is_equal_to("high")
        assert_that(occupancy_high_2).is_equal_to("high")
        
    def test_get_occupancy_low(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        occupancy_low_1 = oc.get_occupancy("2022-01-01")
        
        occupancy_low_2 = oc.get_occupancy("2022-01-02")
        
        assert_that(occupancy_low_1).is_equal_to("low")
        assert_that(occupancy_low_2).is_equal_to("low")

    def test_get_occupancy_None(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        occupancy_1 = oc.get_occupancy("2022-01-03")
        
        occupancy_2 = oc.get_occupancy("2022-01-04")
        
        assert_that(occupancy_1).is_none
        assert_that(occupancy_2).is_none


    def test_get_lowest_price(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        price = oc.get_lowest_price()
        
        assert_that(price).is_equal_to(100.0)

    def test_get_second_lowest_price(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        price = oc.get_second_lowest_price()
        
        assert_that(price).is_equal_to(200.0)

    def test_get_higher_price(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        price = oc.get_higher_price()
        
        assert_that(price).is_equal_to(600.0)

    def test_get_second_higher_price(self):
        
        oc = Occupancy(ticket_prices=self.ticket_prices)

        price = oc.get_second_higher_price()
        
        assert_that(price).is_equal_to(500.0)

    


    
from django.test import TestCase
from django.core.exceptions import ValidationError
from auction_app.models import Auction, Artwork, Customer, Bid


class BidModelTestCase(TestCase):
    def setUp(self):
        self.auction = Auction.objects.create(auction_name="Subasta de Prueba")
        self.artwork = Artwork.objects.create(title="Obra de Arte de Prueba", auction=self.auction, minimum_bid=100.00)
        self.customer = Customer.objects.create(full_name="Cliente de Prueba", email="test@example.com", phone="123456789")

    def test_bid_validation(self):
        # Prueba que una oferta con un valor menor al mínimo genere un ValidationError
        with self.assertRaises(ValidationError):
            Bid.objects.create(auction=self.auction, artwork=self.artwork, customer=self.customer, bid_value=50.00)

from django.test import TestCase
from django.utils import timezone
from .models import Auction, Artwork, Customer, Bid, Admin
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse




class TestModels(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(full_name="John Doe", email="john@example.com", phone="123456789", document_type="ID", document_number="123456789")
        self.auction = Auction.objects.create(auction_name="Test Auction", auction_description="Test Description", start_date=timezone.now(), end_date=timezone.now())
        self.artwork = Artwork.objects.create(auction=self.auction, title="Test Artwork", artist="Test Artist", year_created=2022, dimensions="10x10", material="Oil on Canvas", genre="Abstract", description="Test Description", minimum_bid=100.00)
        self.admin = Admin.objects.create(email="admin@example.com", password="adminpassword")

    def test_auction_creation(self):
        auction = Auction.objects.get(auction_name="Test Auction")
        self.assertEqual(auction.auction_name, "Test Auction")
        self.assertEqual(auction.auction_description, "Test Description")
        self.assertTrue(auction.start_date)
        self.assertTrue(auction.end_date)
        self.assertEqual(auction.status, "active")

    def test_artwork_creation(self):
        artwork = Artwork.objects.get(title="Test Artwork")
        self.assertEqual(artwork.title, "Test Artwork")
        self.assertEqual(artwork.artist, "Test Artist")
        self.assertEqual(artwork.year_created, 2022)
        self.assertEqual(artwork.dimensions, "10x10")
        self.assertEqual(artwork.material, "Oil on Canvas")
        self.assertEqual(artwork.genre, "Abstract")
        self.assertEqual(artwork.description, "Test Description")
        self.assertEqual(artwork.minimum_bid, 100.00)
        self.assertEqual(artwork.status, "active")

    def test_customer_creation(self):
        customer = Customer.objects.get(full_name="John Doe")
        self.assertEqual(customer.full_name, "John Doe")
        self.assertEqual(customer.email, "john@example.com")
        self.assertEqual(customer.phone, "123456789")
        self.assertEqual(customer.document_type, "ID")
        self.assertEqual(customer.document_number, "123456789")

    def test_admin_creation(self):
        admin = Admin.objects.get(email="admin@example.com")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertNotEqual(admin.password, "adminpassword")
        self.assertTrue(admin.password)

    def test_bid_creation(self):
        bid = Bid.objects.create(auction=self.auction, artwork=self.artwork, customer=self.customer, bid_value=200.00, bid_timestamp=timezone.now())
        self.assertEqual(bid.auction, self.auction)
        self.assertEqual(bid.artwork, self.artwork)
        self.assertEqual(bid.customer, self.customer)
        self.assertEqual(bid.bid_value, 200.00)
        self.assertTrue(bid.bid_timestamp)

    def test_invalid_auction_end_date(self):
        with self.assertRaises(ValidationError):
            auction = Auction.objects.create(auction_name="Invalid Auction", auction_description="Test Description", start_date=timezone.now(), end_date=timezone.now()-timezone.timedelta(days=1))
            auction.clean()










class ViewsetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.client.force_authenticate(user=self.admin_user)
        
        # Create a customer
        self.customer = Customer.objects.create(full_name="John Doe", email="john@example.com", phone="123456789", document_type="ID", document_number="123456789")
        
        # Create auction
        self.auction = Auction.objects.create(auction_name="Test Auction", auction_description="Test Description", start_date=timezone.now(), end_date=timezone.now())
        
        # Create artwork
        self.artwork = Artwork.objects.create(auction=self.auction, title="Test Artwork", artist="Test Artist", year_created=2022, dimensions="10x10", material="Oil on Canvas", genre="Abstract", description="Test Description", minimum_bid=100.00)
        
        # Create bid
        self.bid = Bid.objects.create(auction=self.auction, artwork=self.artwork, customer=self.customer, bid_value=200.00, bid_timestamp=timezone.now())

    def test_auction_list(self):
        url = reverse('auction-list')  
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_artwork_list(self):
        url = reverse('artwork-list')
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_list_as_admin(self):
        url = reverse('customer-list')
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_list_as_customer(self):
        url = reverse('customer-list')
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['full_name'], 'John Doe')

    def test_bid_list_as_admin(self):
        url = reverse('bid-list')
        response = self.client.get(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_update_auction(self):
        url = reverse('auction-detail', kwargs={'pk': self.auction.pk})
        new_data = {
            'auction_name': 'Updated Auction',
            'auction_description': 'Updated Description',
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=1)
        }
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_auction = Auction.objects.get(pk=self.auction.pk)
        self.assertEqual(updated_auction.auction_name, 'Updated Auction')
        self.assertEqual(updated_auction.auction_description, 'Updated Description')

    
    def test_delete_auction(self):
        url = reverse('auction-detail', kwargs={'pk': self.auction.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Auction.DoesNotExist):
            Auction.objects.get(pk=self.auction.pk)

    

    def test_delete_artwork(self):
        url = reverse('artwork-detail', kwargs={'pk': self.artwork.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Artwork.DoesNotExist):
            Artwork.objects.get(pk=self.artwork.pk)

    def test_update_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        new_data = {
            'full_name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '987654321',
            'document_type': 'Passport',
            'document_number': '987654321'
        }
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_customer = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(updated_customer.full_name, 'Jane Doe')
        self.assertEqual(updated_customer.email, 'jane@example.com')

    def test_delete_customer(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(pk=self.customer.pk)

    def test_delete_bid(self):
        url = reverse('bid-detail', kwargs={'pk': self.bid.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Bid.DoesNotExist):
            Bid.objects.get(pk=self.bid.pk)



    

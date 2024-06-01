from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Auction, Artwork, Customer, Bid, Admin
from .serializers import AuctionSerializer, ArtworkSerializer, CustomerSerializer, BidSerializer, AdminSerializer
from .permissions import IsAdminUser, IsCustomerOrReadOnly

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAdminUser]

class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = [IsAdminUser]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(id=self.request.user.id)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Bid.objects.all()
        return Bid.objects.filter(customer=self.request.user)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]

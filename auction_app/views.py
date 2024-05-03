from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .serializer import AuctionSerializer, ArtworkSerializer, CustomerSerializer, BidSerializer, AdminSerializer
from .models import Auction, Artwork, Customer, Bid, Admin
from rest_framework.response import Response
from rest_framework import status
from functools import partial

class BasePermissionViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def handle_action(self, request, *args, **kwargs):
        action_handler = getattr(self, f'handle_{self.action}', None)
        if action_handler is not None:
            return action_handler(request, *args, **kwargs)
        return super().handle_action(request, *args, **kwargs)

class AuctionViewSet(BasePermissionViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsAdminUser],
        'destroy': [IsAuthenticated, IsAdminUser]
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArtworkViewSet(BasePermissionViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsAdminUser],
        'destroy': [IsAuthenticated, IsAdminUser]
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CustomerViewSet(BasePermissionViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, partial(IsAdminUser) or partial(is_owner)],
        'destroy': [IsAuthenticated, partial(IsAdminUser) or partial(is_owner)]
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BidViewSet(BasePermissionViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, partial(IsAdminUser) or partial(is_owner)],
        'destroy': [IsAuthenticated, partial(IsAdminUser) or partial(is_owner)]
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Define la función is_owner
def is_owner(request, obj):
    return obj.owner == request.user

class AdminViewSet(BasePermissionViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

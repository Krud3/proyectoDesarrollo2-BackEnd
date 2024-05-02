from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .serializer import AuctionSerializer, ArtworkSerializer, CustomerSerializer, BidSerializer, AdminSerializer
from .models import Auction, Artwork, Customer, Bid, Admin
from rest_framework.response import Response
from rest_framework import status

class PermissionMixin:
    def get_permissions(self):
        if self.request.user.is_superuser:
            return [IsAuthenticated(), IsAdminUser()]  # Los superusuarios pueden hacer cualquier cosa
        else:
            return [IsAdminUser()] 

class AuctionViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
class ArtworkViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    
class CustomerViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == 'create':
            permissions.append(IsAuthenticated())  # Usuarios normales solo pueden crear nuevos registros
        return permissions

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()  # Los superusuarios pueden ver todos los registros
        return Customer.objects.filter(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You do not have permission to update this customer.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class BidViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == 'update':
            permissions.append(IsAuthenticated())  # Usuarios normales solo pueden actualizar el campo bid_value
        return permissions

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Bid.objects.all()  # Los superusuarios pueden ver todos los registros
        return Bid.objects.filter(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You do not have permission to update this bid.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class AdminViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

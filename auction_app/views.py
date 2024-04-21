from rest_framework import viewsets
from .serializer import AuctionSerializer, ArtworkSerializer, CustomerSerializer, BidSerializer, AdminSerializer
from .models import Auction, Artwork, Customer, Bid, Admin
from rest_framework.response import Response
from rest_framework import status


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    def create(self, request, *args, **kwargs):
        auction_name = request.data.get('auction_name')
        auction_description = request.data.get('auction_description')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        status = request.data.get('status')

        if not auction_name:
            return Response({"error": "Auction name cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if len(auction_description) > 255:
            return Response({"error": "Auction description cannot exceed 255 characters."}, status=status.HTTP_400_BAD_REQUEST)

        if end_date and start_date and end_date <= start_date:
            return Response({"error": "The end date must be after the start date."}, status=status.HTTP_400_BAD_REQUEST)

        if status not in ('active', 'inactive'):
            return Response({"error": "Invalid auction status."}, status=status.HTTP_400_BAD_REQUEST)

        existing_auction = Auction.objects.filter(start_date=start_date, end_date=end_date, auction_name=auction_name).exists()
        if existing_auction:
            return Response({"error": "Auction with the same name and dates already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        artist = request.data.get('artist')
        year_created = request.data.get('year_created')
        dimensions = request.data.get('dimensions')
        material = request.data.get('material')
        genre = request.data.get('genre')
        description = request.data.get('description')
        minimum_bid = request.data.get('minimum_bid')

        if not title:
            return Response({"error": "Title cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if len(artist) > 255:
            return Response({"error": "Artist name cannot exceed 255 characters."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(year_created, int) or year_created <= 0:
            return Response({"error": "Year created must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        if len(dimensions) > 50 or len(material) > 100 or len(genre) > 100:
            return Response({"error": "Dimensions, material, or genre exceed maximum length."}, status=status.HTTP_400_BAD_REQUEST)

        if len(description) > 1000:
            return Response({"error": "Description cannot exceed 1000 characters."}, status=status.HTTP_400_BAD_REQUEST)

        if minimum_bid < 0:
            return Response({"error": "Minimum bid must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        phone = request.data.get('phone')

        if not full_name:
            return Response({"error": "Full name cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({"error": "Email cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not phone:
            return Response({"error": "Phone number cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not email_validator(email):
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        if Customer.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bid_value = serializer.validated_data['bid_value']
        minimum_bid = serializer.validated_data['artwork'].minimum_bid
        if bid_value < minimum_bid:
            return Response({"error": "The bid value must be greater than or equal to the minimum bid amount for the artwork."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({"error": "Email cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if not email_validator(email):
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        if Admin.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Add more password complexity validations if needed

        return super().create(request, *args, **kwargs)

# Función para validar el formato del correo electrónico
def email_validator(email):
    import re
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_regex.match(email))

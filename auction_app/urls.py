from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from auction_app import views


router = routers.DefaultRouter()
router.register(r'auctions', views.AuctionViewSet)
router.register(r'artworks', views.ArtworkViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'bids', views.BidViewSet)
router.register(r'admins', views.AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]


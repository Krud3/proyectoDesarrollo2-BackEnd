from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'auctions', views.AuctionViewSet)
router.register(r'artworks', views.ArtworkViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'bids', views.BidViewSet)
router.register(r'admins', views.AdminViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
]



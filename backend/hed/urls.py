# tickets/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, UserProfileView, UserViewSet, EventViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/bookings/', BookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='bookings'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),

]

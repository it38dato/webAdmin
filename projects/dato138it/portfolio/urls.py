from django.urls import include, path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'place', views.PlaceViewSet)
router.register(r'portfolio', views.PortfolioViewSet)
router.register(r'category', views.CategoryViewSet)
urlpatterns = [
    path('', include(router.urls)), #/urls/
]

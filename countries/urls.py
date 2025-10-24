from django.urls import path
from .views import (
    RefreshCountriesView, CountryListView, CountryDetailView, StatusView, ImageView
)

urlpatterns = [
    path('refresh', RefreshCountriesView.as_view(), name='countries-refresh'),
    path('', CountryListView.as_view(), name='countries-list'),
    path('image', ImageView.as_view(), name='countries-image'),
    path('status', StatusView.as_view(), name='countries-status'),
    path('<str:name>', CountryDetailView.as_view(), name='country-detail'),
]

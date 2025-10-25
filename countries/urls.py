from django.urls import path
from .views import (
    RefreshCountriesView, CountryListView, CountryDetailView, StatusView, ImageView
)

urlpatterns = [
    path('countries/refresh', RefreshCountriesView.as_view(), name='countries-refresh'),
    path('countries', CountryListView.as_view(), name='countries-list'),
    path('countries/image', ImageView.as_view(), name='countries-image'),
    path('status', StatusView.as_view(), name='countries-status'),
    path('countries/<str:name>', CountryDetailView.as_view(), name='country-detail'),
]

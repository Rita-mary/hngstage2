import io
import os
import random
from datetime import datetime, timezone

import requests
from django.conf import settings
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone as dj_timezone
from PIL import Image, ImageDraw, ImageFont
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Country
from .serializers import CountrySerializer
from .utils import fetch_json, generate_summary_image, CACHE_IMAGE_PATH, EXCHANGE_URL, RESTCOUNTRIES_URL
# Create your views here.


class RefreshCountriesView(APIView):
    serializer_class = CountrySerializer

    def post(self, request):

        try:
            countries_data = fetch_json(RESTCOUNTRIES_URL)
        except Exception:
            return Response(
                {"error": "External data source unavailable", "details": "Could not fetch data from Countries API"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        try:
            exchange_data = fetch_json(EXCHANGE_URL)
            rates = exchange_data.get("rates") or {}
        except Exception:
            return Response(
                {"error": "External data source unavailable", "details": "Could not fetch data from Exchange Rates API"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        with transaction.atomic():
            now = dj_timezone.now()
            updated_objects = []
            for item in countries_data:
                name = item.get("name")
                capital = item.get("capital")
                region = item.get("region")
                population = item.get("population") or 0
                flag_url = item.get("flag")
                currencies = item.get("currencies") or []
                currency_code = None
                exchange_rate = None
                estimated_gdp = None

                if len(currencies) > 0:
                    currency = currencies[0]
                    currency_code = currency.get("code")
                    if currency_code:
                        exchange_rate = rates.get(currency_code)
                        if exchange_rate in (None, 0):
                            exchange_rate = None
                            estimated_gdp = None
                        else:
                            multiplier = random.randint(1000, 2000)
                            try:
                                estimated_gdp = population * float(multiplier) / exchange_rate
                            except Exception:
                                estimated_gdp = 0

                    else:
                        currency_code = None
                        exchange_rate = None
                        estimated_gdp = 0
                else:
                    currency_code = None
                    exchange_rate = None
                    estimated_gdp = 0

                obj = Country.objects.filter(name__iexact=name).first()
                if obj:
                    obj.capital = capital
                    obj.region = region
                    obj.population = population
                    obj.currency_code = currency_code
                    obj.exchange_rate = exchange_rate
                    obj.estimated_gdp = estimated_gdp
                    obj.flag_url = flag_url
                    obj.last_refreshed_at=now
                    obj.save()
                else:
                    obj = Country.objects.create(
                        name=name,
                        capital=capital,
                        region=region,
                        population=population,
                        currency_code=currency_code,
                        exchange_rate=exchange_rate,
                        estimated_gdp=estimated_gdp,
                        flag_url=flag_url,
                        last_refreshed_at=now
                    )
                updated_objects.append(obj)
            total_countries = Country.objects.count()
            top5_countries = Country.objects.order_by('-estimated_gdp')[:5]
            timestamp_iso = now.astimezone(timezone.utc).isoformat()
            generate_summary_image(total_countries, top5_countries, timestamp_iso)
            return Response({"message": "Refresh successful", "total_countries": total_countries, "last_refreshed_at": timestamp_iso}, status=status.HTTP_200_OK)
        
class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        region = self.request.query_params.get('region')
        sort = self.request.query_params.get('sort')
        currency = self.request.query_params.get('currency')
        if region:
            queryset = queryset.filter(region__iexact=region)
        if sort == "gdp_asc":
            queryset = queryset.order_by('estimated_gdp')
        elif sort == "gdp_desc":
            queryset = queryset.order_by('-estimated_gdp')
        if currency:
            queryset = queryset.filter(currency_code__iexact=currency)
        return queryset
    
class CountryDetailView(APIView):

    def get(self, request, name):
        country = Country.objects.filter(name__iexact=name).first()
        if not country:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, name):
        country = Country.objects.filter(name__iexact=name).first()
        if not country:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatusView(APIView):

    def get(self, request):
        total = Country.objects.count()
        last = Country.objects.order_by('-last_refreshed_at').first()
        last_ts = last.last_refreshed_at if last else None
        if last_ts:
            last_iso = last_ts.astimezone(timezone.utc).isoformat()
        else:
            last_iso = None
        return Response({"total_countries": total, "last_refreshed_at": last_iso})
    
class ImageView(APIView):

    def get(self, request):
        if not os.path.exists(CACHE_IMAGE_PATH):
            return Response(
                {"error": "Summary image not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return FileResponse(open(CACHE_IMAGE_PATH, 'rb'), content_type='image/png')
    


from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ('id','last_refreshed_at',)

    def validate(self, data):
        errors = {}
        if self.instance is None and not data.get('name'):
            errors['name'] = 'is required'
        if data.get('population') is None:
            errors['population'] = 'is required'
        if self.instance is None and not data.get('currency_code'):
            errors['currency_code'] = 'is required'
        if errors:
            raise serializers.ValidationError(errors)
        return data

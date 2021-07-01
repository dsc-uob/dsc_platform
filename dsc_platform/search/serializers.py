from rest_framework import serializers
from .models import Tag, SearchHistory


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SearchHistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'

from rest_framework import serializers
from .models import Product,Review

class ProductSerializer(serializers.ModelSerializer):
    #data that we want to make it in the form of JSON
    class Meta: 
        model = Product
        fields = "__all__"
        # fields = ('name', 'price') spécifier dans JSON what we want to return
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
          model = Review
          fields = "__all__"
          
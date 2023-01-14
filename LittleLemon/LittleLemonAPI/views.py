from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.response import Response 
from rest_framework import viewsets 
from .models import MenuItem 
from .serializers import MenuItemSerializer  
# Create your views here.
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','inventory']
    search_fields=['title','category__title']
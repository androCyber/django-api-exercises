from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from .models import Category 
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items=MenuItem.objects.select_related('category').all()
        category_name=request.query_params.get('category')
        to_price=request.query_params.get('to_price')
        search=request.query_params.get('search')
        ordering=request.query__params.get('ordering')
        perpage=request.query__params.get('perpage',default=2)
        page=request.query__params.get('page',default=1)
        
        if category_name:
            items=items.filter(category__title=category_name) #double underscore category and title
        
        if to_price:
            items=items.filter(price=to_price)    #price__lte means less than or equal
        
        if search:
            items=items.filter(title__contains=search) #icontaints and istartswith are case insentivite
        
        if ordering:
            ordering_fields=ordering.split(",")
            items=items.order_by(*ordering_fields)
        
        paginator=Paginator(items,per_page=perpage)
        try:
            items=paginator.page(number=page)
        except EmptyPage:
            items=[]
        
        serialized_item=MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)
    
    if request.method == 'POST':
        serialized_item=MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    
@api_view()
def single_item(request,id):
    item=get_object_or_404(MenuItem,pk=id)
    serialized_item=MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})


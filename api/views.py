from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Products
from .serializer import ProductSerializer

@cache_page(60*15)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_list(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_details(request, pk):
    try:
        if cache.get(pk):
            product_id = Products.objects.get(pk=pk)
            cache.get(pk)
            print("from cache")
        else:
            pk = cache.set(pk, 30)
            product_id = Products.objects.get(pk=pk)
            print("from db")
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product_id)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = ProductSerializer(product_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_UPDATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
    if request.method == 'DELETE':
        product_id.delete()
        return Response(serializer.data, status=status.HTTP_204_DELTED)
    
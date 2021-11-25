from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.http import response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view

from banrau.models import Product, Category
from banrau.serializers import UserSerializer, GroupSerializer, ProductSerializer, CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description_icontains= query))
        serializer = ProductSerializer(products, many = True)
        return response(serializer.data)
    else:
        return response({"products": []})

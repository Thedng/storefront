from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer
from .filters import ProductFilter

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with a order.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs) 


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(product=kwargs['pk']).count() > 0:
            return Response({'error':'collection cannot be deleted because it contains one or more proucts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewset(ModelViewSet): 

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewset(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewset(ModelViewSet):
    
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
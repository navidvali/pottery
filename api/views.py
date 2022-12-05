from rest_framework.response import Response
from rest_framework.decorators import api_view
from shop.models import Products
from .serializers import ProductsSerializer

@api_view(['GET'])
def getcats(request):
    # products = Products.objects.all()
    p = Paginator(Products.objects.order_by("-created_on"), 6)
    page = request.GET.get('page')
    products_paginated = p.get_page(page)

    serializer = ProductsSerializer(products_paginated, many=True)
    return Response(serializer.data)

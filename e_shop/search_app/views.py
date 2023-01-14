from django.shortcuts import render
from e_shopee.models import Product
from django.db.models import Q


def search_result(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
        return render(request, 'search.html', {'query': query, 'products': products})
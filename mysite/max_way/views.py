from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import servise


def index(request):
    if request.GET:
        product = servise.get_product_by_id(request.GET.get("product_id", 0))
        print(product)
        return JsonResponse(product)

    categories = servise.get_category()
    products = servise.get_product()
    ctx = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'fronted/index.html', ctx)


def order(request):
    return render(request, 'fronted/order.html')

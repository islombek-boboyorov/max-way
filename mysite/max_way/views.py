from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import servise
import json
from dashboard.forms import *
from datetime import datetime


def index(request):
    if request.GET:
        product = servise.get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

    # if request.POST:
    #     products = request.POST.getlist("product")
    #     model = Order()
    #     for p in products:
    #         model.products.add(Product.objects.get(pk=int(p)))
    #
    #     return redirect("order", order_id=model.pk)

    orders = []
    orders_list = request.COOKIES.get("orders")
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": val,
                }
            )
    categories = servise.get_category()
    products = servise.get_product()
    ctx = {
        "categories": categories,
        "products": products,
        "orders": orders
    }
    response = render(request, 'fronted/index.html', ctx)
    return response


def order_save(request):
    if request.POST:
        new_order = Order()
        new_order.total_price = request.COOKIES.get("total_price", 0)
        new_order.products = request.COOKIES.get("orders", {})
        new_order.status = 1
        new_order.created_at = datetime.now()
        new_order.save()

    response = redirect("order")
    response.set_cookie("total_price", 0)
    response.set_cookie("orders", dict())

    return response


def order(request):
    return render(request, 'fronted/order.html')

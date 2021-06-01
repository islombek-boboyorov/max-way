from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import servise
from .models import *
from dashboard.forms import *


def index(request):
    if request.GET:
        product = servise.get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

    if request.POST:
        products = request.POST.getlist("product")
        model = Order()
        b = 0
        for p in products:
            c = servise.get_product_price(int(p))["price"]
            b += c
        if b != 0:
            model.total_price = b
            model.save()
        else:
            return redirect('index')

        for p in products:
            model.products.add(Product.objects.get(pk=int(p)))
        return redirect("order", order_id=model.pk)

    categories = servise.get_category()
    products = servise.get_product()
    ctx = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'fronted/index.html', ctx)


def order(request, order_id):
    model = User()
    form = UserForm(request.POST, instance=model)
    order = Order.objects.get(pk=order_id)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    ctx = {
        "order": order
    }
    return render(request, 'fronted/order.html', ctx)

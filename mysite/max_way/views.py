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
        model.total_price = b
        model.save()
        for p in products:
            model.products.add(Product.objects.get(pk=int(p)))

    categories = servise.get_category()
    products = servise.get_product()
    ctx = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'fronted/index.html', ctx)


def order(request):
    # count = servise.get_order_max_id()['max']
    model = User.objects.all()
    form = UserForm(request.POST, instance=model)
    print("A")
    if request.POST:
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'fronted/order.html', ctx)

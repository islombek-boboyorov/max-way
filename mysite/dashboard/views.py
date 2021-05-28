from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import servise
from .forms import *
from max_way.models import *



def login_required_decorator(f):
    return login_required(f, login_url="login")


@login_required_decorator
def dashboard_page(request):
    return render(request, 'dashboard/index.html')


def dashboard_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('login')


def user_list(request):
    users = servise.get_user()
    # users = User.objects.all()
    print(users)
    ctx = {
        "users": users
    }
    return render(request, 'dashboard/user/list.html', ctx)


def user_create(request):
    model = User()
    form = UserForm(request.POST, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/user/form.html', ctx)


def user_edit(request, pk):
    model = User.objects.get(id=pk)
    form = UserForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('user_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/user/form.html', ctx)


def user_delete(request, pk):
    model = User.objects.get(id=pk)
    model.delete()
    return redirect('user_list')


def order_list(request):
    orders = servise.get_order()
    ctx = {
        "orders": orders
    }
    return render(request, 'dashboard/order/list.html', ctx)


def order_create(request):
    model = Order()
    form = OrderForm(request.POST, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('order_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/order/form.html', ctx)


def order_edit(request, pk):
    model = Order.objects.get(id=pk)
    form = OrderForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('order_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/order/form.html', ctx)


def order_delete(pk):
    model = Order.objects.get(id=pk)
    model.delete()
    return redirect('order_list')


def category_list(request):
    categories = servise.get_category()
    ctx = {
        "categories": categories
    }
    return render(request, 'dashboard/category/list.html', ctx)


def category_create(request):
    model = Category()
    form = CategoryForm(request.POST, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/category/form.html', ctx)


def category_edit(request, pk):
    model = Category.objects.get(id=pk)
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/category/form.html', ctx)


def category_delete(request, pk):
    model = Category.objects.get(id=pk)
    model.delete()
    return redirect('category_list')


def product_list(request):
    products = servise.get_product()
    ctx = {
        "products": products
    }
    return render(request, 'dashboard/product/list.html', ctx)


def product_create(request):
    model = Product()
    form = ProductForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/product/form.html', ctx)


def product_edit(request, pk):
    model = Product.objects.get(id=pk)
    form = ProductForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/product/form.html', ctx)


def product_delete(request, pk):
    model = Product.objects.get(id=pk)
    model.delete()
    return redirect('product_list')

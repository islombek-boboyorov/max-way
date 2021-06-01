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
    count_cat = servise.get_category_count()['name']
    count_prod = servise.get_product_count()['title']
    categories = servise.news_count()
    status = servise.get_status_info()
    stat_1 = servise.get_status_1()[0]
    print(stat_1)
    stat_2 = servise.get_status_2()[0]
    stat_3 = servise.get_status_3()[0]
    ctx = {
        "count_cat": count_cat,
        "count_prod": count_prod,
        "categories": categories,
        "status": status,
        "stat_1": stat_1,
        "stat_2": stat_2,
        "stat_3": stat_3,
    }
    return render(request, 'dashboard/index.html', ctx)


def status(request, pk):
    model = Order.objects.get(id=pk)
    form = OrderForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            print(form.errors)
    ctx = {
        "form": form,
    }
    return render(request, 'dashboard/form.html', ctx)


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

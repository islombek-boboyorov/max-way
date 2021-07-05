from ..models import User, Category, Product, Order, Bot_user
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, UserSerializer, Bot_userSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from . import servise
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        category = servise.get_category()
        return Response(category, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        product = servise.get_product()
        return Response(product, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def product_details(request, pk):
    if request.method == "GET":
        try:
            product = Product.objects.get(id=pk)
        except:
            raise NotFound(f"Product with pk = {pk} not found!")
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        try:
            product = Product.objects.get(id=pk)
        except:
            raise NotFound(f"Product with pk = {pk} not found!")
        serializer = ProductSerializer(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        try:
            product = Product.objects.get(id=pk)
        except:
            raise NotFound(f"Product with pk = {pk} not found!")
        product.delete()
        return Response({"delete": f"Product with pk = {pk} has been deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def order_list(request):
    if request.method == "GET":
        order = servise.get_order()
        return Response(order, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def order_details(request, pk):
    if request.method == "GET":
        try:
            order = Order.objects.get(id=pk)
        except:
            raise NotFound(f"Order with pk = {pk} not found!")
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        try:
            order = Order.objects.get(id=pk)
        except:
            raise NotFound(f"Order with pk = {pk} not found!")
        serializer = OrderSerializer(data=request.data, instance=order)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        try:
            order = Order.objects.get(id=pk)
        except:
            raise NotFound(f"Order with pk = {pk} not found!")
        order.delete()
        return Response({"delete": f"Order with pk = {pk} has been deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def user_list(request):
    if request.method == "GET":
        user = servise.get_user()
        return Response(user, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def user_details(request, pk):
    if request.method == "GET":
        try:
            user = User.objects.get(id=pk)
        except:
            raise NotFound(f"User with pk = {pk} not found!")
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        try:
            user = User.objects.get(id=pk)
        except:
            raise NotFound(f"User with pk = {pk} not found!")
        serializer = UserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        try:
            user = User.objects.get(id=pk)
        except:
            raise NotFound(f"User with pk = {pk} not found!")
        user.delete()
        return Response({"delete": f"User with pk = {pk} has been deleted successfully!"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def bot_list(request):
    if request.method == "GET":
        bot = servise.get_bot()
        return Response(bot, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = Bot_userSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT", "DELETE"])
def bot_details(request, pk):
    if request.method == "GET":
        try:
            bot = Bot_user.objects.get(id=pk)
        except:
            raise NotFound(f"Bot_user with pk = {pk} not found!")
        serializer = UserSerializer(bot, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        try:
            bot = Bot_user.objects.get(id=pk)
        except:
            raise NotFound(f"Bot_user with pk = {pk} not found!")
        serializer = UserSerializer(data=request.data, instance=bot)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        try:
            bot = Bot_user.objects.get(id=pk)
        except:
            raise NotFound(f"Bot_user with pk = {pk} not found!")
        bot.delete()
        return Response({"delete": f"Bot_user with pk = {pk} has been deleted successfully!"}, status=status.HTTP_200_OK)

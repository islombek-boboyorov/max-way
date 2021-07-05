from . import views
from django.urls import path, include


urlpatterns = [

    path('category/', views.category_list),

    path('product/', views.product_list),
    path('product/<int:pk>/', views.product_details),

    path('order/', views.order_list),
    path('order/<int:pk>/', views.order_details),

    path('user/', views.user_list),
    path('user/<int:pk>/', views.user_details),

    path('bot/', views.bot_list),
    path('bot/<int:pk>/', views.bot_details),
]

from django.urls import path, include
from . import views
from max_way.api import urls

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:order_id>/order/', views.order, name="order"),
    path('order/save/', views.order_save, name="order-save"),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include(urls))
]

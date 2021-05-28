from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('order/', views.order, name="order"),
    path('dashboard/', include('dashboard.urls')),
]

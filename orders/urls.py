from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registration, name="registration"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name='logout'),
    path("order/<dish>/<int:kindid>", views.order, name='order'),
    path("order_delete/<int:orderid>", views.order_delete, name='order_delete'),
    path("purchase", views.purchase, name='purchase'),
    path('myorders', views.myorders, name='myorders')
]

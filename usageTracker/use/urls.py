from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add/", views.add, name="add"),
    path("check/<int:year>/<int:month>", views.check, name="check"),
    path("details/<int:year>/<int:month>", views.details, name="details")
]
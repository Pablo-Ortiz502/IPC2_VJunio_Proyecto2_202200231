from django.urls import path
from .views import login_view, home_view,test_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("homeAdmin/", home_view, name="homeAdmin"),
    path("test/",test_view, name="test"),
]
from django.urls import path
from .views import login_view, home_view,test_view,upload_xml_view,users_view,yo_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("homeAdmin/", home_view, name="homeAdmin"),
    path("test/",test_view, name="test"),
    path("homeAdmin/setted",upload_xml_view, name="setted"),
    path("homeAdmin/users",users_view, name="users"),
    path("homeAdmin/yo", yo_view, name="yo")
]
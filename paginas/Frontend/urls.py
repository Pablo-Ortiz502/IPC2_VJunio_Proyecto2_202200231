from django.urls import path
from .views import login_view, home_view,test_view,upload_xml_view,users_view,yo_view,time_view,notes_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("home/", home_view, name="homeAdmin"),
    path("test/",test_view, name="test"),
    path("home/setted",upload_xml_view, name="setted"),
    path("home/users",users_view, name="users"),
    path("home/yo", yo_view, name="yo"),
    path("home/times", time_view, name="times"),
    path("home/notesT", notes_view, name="notesT")
]
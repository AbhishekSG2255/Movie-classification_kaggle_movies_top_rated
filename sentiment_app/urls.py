from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_movie, name="search_movie"),
    path("predict/", views.predict, name="predict"),
    path("add_review/", views.add_review, name="add_review"),
]


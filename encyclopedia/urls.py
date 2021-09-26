from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  #default url
    path("search", views.find_page, name="search"),
    path("add", views.add_page, name="add"),
    path("dd", views.dd, name="dd"),
    path("edit_page_data", views.edit_page_data, name="edit_page_data"),
    path("save_edit", views.save_edit_changes, name="save_edit"),
    path("random", views.entry_random, name="random"),
    path("<str:entry>", views.get_page, name="get_page")


   ]

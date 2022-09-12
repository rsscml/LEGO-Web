# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('tables_data', views.tables_data, name='tables_data'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages')

]

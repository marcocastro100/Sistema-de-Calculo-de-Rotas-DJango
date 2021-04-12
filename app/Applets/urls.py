from django.urls import path, include #way to redirect web page to the project tree structure
from . import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register('api',views.AppletView)

urlpatterns = [
    #GUI
    path('',views.applets_list,name='list'),
    path('<int:id>/',views.applets_detail,name='detail'), #when a integer (id) is in the url, redirect to detail the corresponding id object in the database
    path('create/',views.applets_create,name='create'),
    path('delete/<int:id>/',views.applets_delete,name='delete'),
    path('download/<int:id>/',views.applets_download,name='download'),
    path('search/',views.applets_search,name='search'),
    
    #API na mão..
    # path('api/',views.api_list.as_view(),name='api_list'),
    # path('api/<int:id>/',views.api_detail.as_view(),name='api_detail'),
    # path('api/search/',views.api_search.as_view(),name='api_search'),

    path('api/',include(router.urls)),

]

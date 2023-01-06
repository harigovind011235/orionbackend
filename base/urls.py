
from django.urls import path
from . import views


urlpatterns = [
    path('',views.getRoutes,name="routes"),
    path('blogs/',views.getBlogs,name="blogs")
]
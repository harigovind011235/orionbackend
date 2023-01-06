
from django.urls import path
from . import views

urlpatterns = [
    path('routes',views.getDailyReadRoutes,name="dailyread-routes"),
    path('blogs',views.getBlogs,name="blogs"),
    path('news',views.getNews,name="news")
]
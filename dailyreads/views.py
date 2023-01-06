
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer,NewsSerializer
from .models import Blogs,News

# Create your views here.

@api_view(['GET'])
def getDailyReadRoutes(request):
    routes = [
        {'GET': 'api/dailyreads/news'},
        {'GET': 'api/dailyreads/blogs'},
    ]

    return Response(routes)

@api_view(['GET'])
def getBlogs(request):
    blogs = Blogs.objects.all()
    serializer = BlogSerializer(blogs,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getNews(request):
    news = News.objects.all()
    serializer = NewsSerializer(news,many=True)
    return Response(serializer.data)
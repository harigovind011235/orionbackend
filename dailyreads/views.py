
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer,NewsSerializer,QuoteSerializer
from .models import Blogs,News,Quote

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


@api_view(['GET'])
def getQuote(request):
    quote = Quote.objects.order_by('?').first()
    serializer = QuoteSerializer(quote)
    return Response(serializer.data)
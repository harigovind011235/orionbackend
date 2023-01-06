
from .blogs import blogs
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'base/blogs/',
        'base/news/',
        'base/team/',
        'base/dailyhours/',
        'base/remainingleaves/',
        'base/leavestatus/',

    ]
    return Response(routes)

@api_view(['GET'])
def getBlogs(request):
    return Response(blogs)
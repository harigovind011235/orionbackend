import os
from dotenv import load_dotenv
load_dotenv('.env')
import logging
logger = logging.getLogger('my_json')
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
    logger.info('Sign up', extra={'referral_code': '52d6ce'})
    logger.error('Request failed', exc_info=True)
    return Response(routes)

@api_view(['GET'])
def getBlogs(request):
    return Response(blogs)
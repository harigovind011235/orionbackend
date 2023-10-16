
import logging
import time
import gzip
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print(f"Incoming Request: {request.method} {request.path}")
        response = self.get_response(request)
        print(f"Outgoing Request: {response.status_code}")
        return response


class RequestTimingMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        print(f"Request took {end_time - start_time:.6f} seconds")
        return response


class GzipMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        if "gzip" in request.META.get('HTTP_ACCEPT_ENCODING',''):
            response.content = gzip.compress(response.content)
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = str(len(response.content))
        return response


class SimpleBaseAuthMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if not request.user.is_authenticated:
            return redirect('login/')
        response = self.get_response(request)
        return response

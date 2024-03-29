import os
import multiprocessing
from dotenv import load_dotenv
load_dotenv('.env')


port = os.getenv('PORT')

wsgi_app = "backend.wsgi:application"

workers = multiprocessing.cpu_count() * 2 + 1

bind = f"0.0.0.0:{port}"

accesslog = "/var/log/gunicorn/orionbackend_access.log"
errorlog = "/var/log/gunicorn/orionbackend_error.log"

capture_output = True

daemon = False
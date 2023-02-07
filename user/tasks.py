from __future__ import absolute_import,unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Employee,DailyHour

logger = get_task_logger(__name__)


@shared_task
def printmsg():
    print("Celery is Working Fine")


@shared_task
def getAbsentees():
    today = timezone.now().date()
    presentees = DailyHour.objects.filter(created__date=today).values_list('employee', flat=True)
    all_employees = Employee.objects.all()
    absentees = list(all_employees.exclude(id__in=presentees).values_list('name',flat=True))
    if absentees:
        send_mail(
            'Today\'s Absentees',
            'Employees - ' + str(absentees),
            settings.EMAIL_HOST_USER,
            ['harigovindyearzero@gmail.com'],
            fail_silently=False,
        )
    else:
        send_mail(
            'Today\'s Absentees',
            'No Absentees Today',
            settings.EMAIL_HOST_USER,
            ['harigovindyearzero@gmail.com'],
            fail_silently=False,
        )


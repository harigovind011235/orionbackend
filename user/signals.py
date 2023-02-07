
from django.contrib.auth.models import User
from .models import Employee,RemainingLeave,Leave
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):

    if created:
        user = instance
        profile = Employee.objects.create(user=user,name=user.username)
        profile.save()
        leaves = RemainingLeave.objects.create(employee=profile)
        leaves.save()

# @receiver(post_delete,sender=Employee)
# def DeleteProfile(sender,instance,**kwargs):
#     user = instance.user
#     user.delete()


@receiver(pre_save,sender=Leave)
def getPreviousLeaveStatus(sender,instance,**kwargs):

    employee = instance.employee
    previous_status = instance._meta.get_field('status').get_default()
    current_status = instance.status
    if previous_status == False and current_status == True:
        leave_table = instance
        leavetype = leave_table.leave_type
        noofleaves = leave_table.no_of_leaves_required
        remainingleaves = employee.remainingleave
        if leavetype == '1':
            remainingleaves.casual_leave -= int(noofleaves)
        elif leavetype == '2':
            remainingleaves.sick_leave -= int(noofleaves)
        elif leavetype == '3':
            remainingleaves.emergency_leave -= int(noofleaves)
        elif leavetype == '4':
            remainingleaves.comp_off -= int(noofleaves)
        elif leavetype == '5':
            remainingleaves.optional_holidays -= int(noofleaves)
        elif leavetype == '6':
            remainingleaves.casual_leave = remainingleaves.casual_leave - 0.5

        remainingleaves.save()

@receiver(post_save,sender=Leave)
def AppliedLeaveMail(sender,instance,created,**kwargs):
    if created:
        leave_instance = instance
        employee = instance.employee
        # Get the name from choice field
        leave_type = Leave.LEAVE_CHOICES[int(leave_instance.leave_type) - 1][1]
        # Convert the date time to date
        datetime_str = str(instance.created)
        datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f%z")
        created_date = datetime_object.date()

        subject = 'Leave Applied by {}'.format(employee.name)
        message = ' {} applied for a leave:- \n \n Leave Type:- {}\n Date of Leave:- {} \n Leave Reason:- {}\n No of Leaves:- {}\n Applied on:- {}'.format(employee.name.capitalize(), leave_type.capitalize(),instance.date_of_leave,instance.leave_notes, instance.no_of_leaves_required, created_date,)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['karthikaa@labglo.com'],
            fail_silently=False
        )
    else:
        employee = instance.employee
        leave_type = Leave.LEAVE_CHOICES[int(instance.leave_type) - 1][1]
        datetime_str = str(instance.created)
        datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f%z")
        created_date = datetime_object.date()
        subject = 'Leave Approved'
        message = ' Name:- {} \n Leave Type:- {}\n Date of Leave:- {} \n Leave Reason:- {}\n No of Leaves:- {}\n Applied on:- {}'.format(employee.name.capitalize(), leave_type.capitalize(),instance.date_of_leave,instance.leave_notes, instance.no_of_leaves_required, created_date,)

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [employee.email],
            fail_silently=False
        )
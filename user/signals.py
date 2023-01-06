
from django.contrib.auth.models import User
from .models import Employee,RemainingLeave,Leave
from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver


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

        remainingleaves.save()
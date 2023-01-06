
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator


# Create your models here.

numeric = RegexValidator(r'^[0-9+]', 'Only digit characters.')



class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    bio = models.TextField(null=True,blank=True)
    username = models.CharField(max_length=20)
    location = models.CharField(max_length=30)
    profile_image = models.ImageField(null=True,blank=True)
    contact_no = models.CharField(max_length=10, blank=True, validators=[numeric])
    alternate_contact = models.CharField(max_length=10, null=True,blank=True, validators=[numeric])
    blood_group = models.CharField(max_length=20,null=True,blank=True)
    designation = models.CharField(max_length=20,null=True,blank=True)
    date_of_joining = models.DateField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=True,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.user.username)


class Leave(models.Model):

    LEAVE_CHOICES = (
        ("1", "causal leave"),
        ("2", "sick leave"),
        ("3", "emergency leave"),
        ("4", "Comp OFF"),
        ("5", "optional holiday"),
    )
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    leave_type = models.CharField(max_length=20,choices=LEAVE_CHOICES,default='1')
    date_of_leave = models.DateField(null=True,blank=True)
    no_of_leaves_required = models.IntegerField(default=1,validators=[MaxValueValidator(3),MinValueValidator(1)])
    leave_notes = models.TextField(null=True,blank=True)
    status = models.BooleanField(default=False,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str("Employee - {employee}, Leave Applied - {date_of_leave}, Status - {status} ".format(employee=self.employee,date_of_leave=str(self.date_of_leave),status=str(self.status)))


class RemainingLeave(models.Model):
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE,null=True,blank=True)
    casual_leave = models.IntegerField(default=12)
    sick_leave = models.IntegerField(default=10)
    emergency_leave = models.IntegerField(default=2)
    comp_off = models.IntegerField(default=0)
    optional_holidays = models.IntegerField(default=2)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.employee.name)


class DailyHour(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    checkin = models.CharField(max_length=10,null=True,blank=True)
    checkout = models.CharField(max_length=10,null=True,blank=True)
    hours_perday = models.CharField(max_length=20,null=True,blank=True)
    date_of_checkin = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.employee.name + " " + self.date_of_checkin)




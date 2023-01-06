from django.contrib import admin
from .models import Leave,Employee,DailyHour,RemainingLeave
from django_admin_listfilter_dropdown.filters import (DropdownFilter)
from django.contrib.admin import DateFieldListFilter
from datetime import datetime
# date_format = '%A, %B %d, %Y'

# Register your models here.

class LeaveAdmin(admin.ModelAdmin):
    # Order the posts by the `published_date` field in descending order
    ordering = ['-date_of_leave']
    list_filter = [
        ('employee__name', DropdownFilter),
        ('status',DropdownFilter),
    ]
    search_fields = ['employee__name']


class EmployeeAdmin(admin.ModelAdmin):
    list_filter = [
        ('name',DropdownFilter),
    ]
    search_fields = ['name']


class RemainingLeaveAdmin(admin.ModelAdmin):
    list_filter = [
        ('employee__name',DropdownFilter),
    ]
    search_fields = ['employee__name']


class DailyHourAdmin(admin.ModelAdmin):
    list_filter = (
        ('date_of_checkin', DateFieldListFilter),)


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(DailyHour,DailyHourAdmin)
admin.site.register(Leave,LeaveAdmin)
admin.site.register(RemainingLeave,RemainingLeaveAdmin)



from rest_framework import serializers
from .models import Employee,Leave,DailyHour,RemainingLeave


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'



class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'


class DailyHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyHour
        fields = '__all__'

class RemainingLeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemainingLeave
        fields = '__all__'

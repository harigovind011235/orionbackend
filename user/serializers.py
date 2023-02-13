
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

class PendingLeaveSerializer(serializers.Serializer):
    employee_name = serializers.SerializerMethodField()
    employee_id = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()


    def get_employee_name(self, obj):
        return obj['employee__name']

    def get_count(self, obj):
        return obj['count']

    def get_employee_id(self,obj):
        return obj['employee_id']


class AllLeaveSerializer(serializers.ModelSerializer):
    employee_details = PendingLeaveSerializer(source='*')
    class Meta:
        model = Leave
        fields = '__all__'


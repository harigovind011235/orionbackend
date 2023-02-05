
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Employee,DailyHour,Leave,RemainingLeave
from .serializers import EmployeeSerializer,LeaveSerializer,DailyHourSerializer,RemainingLeavesSerializer, PendingLeaveSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import json


# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.employee.name
        data['userid'] = self.user.employee.id
        data['is_staff'] = self.user.is_staff
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getUserRoutes(request):
    routes = [
        {'GET':'api/user/all'},
        {'GET':'api/user/id'},
        {'POST': 'api/user/id'},
        {'GET':'api/user/id/leavestatus'},
        {'POST': 'api/user/id/leavestatus'},
        {'DELETE': 'api/user/id/deleteleave'},
        {'GET':'api/user/id/dailyhours'},
        {'POST': 'api/user/id/dailyhours'},
        {'POST': 'api/user/id/changepassword'},
        {'PUT': 'api/user/id/updateprofile'},
        {'PUT': 'api/user/id/leavetable'},
    ]

    return Response(routes)

@api_view(['GET'])
def getAllPendingLeaves(request):

    class AllPendingLeavesPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    paginator = AllPendingLeavesPagination()
    pending_leaves = Leave.objects.filter(status=False).values('employee__name','employee_id').annotate(count=Count('employee_id'))
    result_page = paginator.paginate_queryset(pending_leaves, request)
    serializer = PendingLeaveSerializer(result_page,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLeavesForApproval(request,id):

    employee = Employee.objects.get(pk=id)
    employee_pending_leaves = employee.leave_set.filter(status=False)
    pending_leaves = []
    for leave in employee_pending_leaves:
        data = {}
        data['leave_applied'] = leave.date_of_leave
        data['leave_notes'] = leave.leave_notes
        data['no_of_leaves'] = leave.no_of_leaves_required
        data['leave_type'] = leave.leave_type
        data['leave_id'] = leave.id
        pending_leaves.append(data)

    return Response(pending_leaves)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAllUsers(request):
    class EmployeePagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    paginator = EmployeePagination()
    all_employees = Employee.objects.all().order_by('date_of_joining')
    result_page = paginator.paginate_queryset(all_employees, request)
    serializer = EmployeeSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request,id):
    profile = Employee.objects.get(pk=id)
    serializer = EmployeeSerializer(profile,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setChangePassword(request,id):
    if request.method == 'POST':
        employee = Employee.objects.get(pk=id)
        user = employee.user

        try:
            changepassword_data = json.loads(request.body)
        except:
            changepassword_data = None
        if changepassword_data:
            current_password = changepassword_data.get('current_password')
            new_password = changepassword_data.get('new_password')


            if employee.user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password was successfully updated!')

                # Update the session authentication hash to prevent the user from being logged out
                update_session_auth_hash(request, user)
                return Response("Successfully change the password")
            else:
                return Response("Password doesn't match")


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getLeaves(request,id):

    employee = Employee.objects.get(pk=id)
    if request.method == 'POST':
        leave_table = Leave(employee=employee)
        try:
            apply_leave_data = json.loads(request.body)
        except:
            apply_leave_data = None

        leave_table.employee = employee
        leave_table.leave_type = apply_leave_data.get('leaveType')
        leave_table.leave_notes = apply_leave_data.get('leaveNotes')
        leave_table.date_of_leave = apply_leave_data.get('leaveDate')
        leave_table.no_of_leaves_required = apply_leave_data.get('noOfLeaves')
        leave_table.save()

        return Response("Success")

    employee_leaves = employee.leave_set.all()
    serializer = LeaveSerializer(employee_leaves,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRemainingLeaves(request,id):
    employee = Employee.objects.get(pk=id)
    remaining_leaves = RemainingLeave.objects.get(employee=employee)
    serializer = RemainingLeavesSerializer(remaining_leaves,many=False) if remaining_leaves else {}
    if serializer:
        return Response(serializer.data)
    else:
        return Response({})


@api_view(['PUT'])
def updateEmployeeLeave(request,id):
    employee_leave = Leave.objects.get(pk=id)
    try:
        employee_leave.status = True
        employee_leave.save()
    except:
        employee_leave.status = False
        return Response("Failed")

    return Response("Success")

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setUpdateProfile(request, id):
    if request.method == 'PUT':
        employee = Employee.objects.get(pk=id)

        try:
            profile_data = json.loads(request.body)
        except:
            profile_data = None
        if request.FILES:
            employee.profile_image = request.FILES.get('profile_image')
            employee.save()
        if profile_data:
            for key, value in profile_data.items():
                setattr(employee, key, value)
                employee.save()
        return Response("Success")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leavesDelete(request,id):

    employee_leave = Leave.objects.get(pk=id)

    if request.method == 'DELETE':
        if employee_leave.status == False:
            employee_leave.delete()
            return Response("deleted one leave")
        else:
            return Response("Already Approved")


@api_view(['GET','POST','PUT'])
@permission_classes([IsAuthenticated])
def getDailyHours(request,id):

    employee = Employee.objects.get(pk=id)
    today = timezone.localtime().date()
    if request.method == 'POST':
        daily_hour_table = DailyHour(employee=employee)
        entry_exists = DailyHour.objects.filter(created__date=today,employee=employee).exists()
        if not entry_exists:
            daily_hour_data = json.loads(request.body)
            daily_hour_table.employee = employee
            daily_hour_table.checkin = daily_hour_data.get('loginTime')
            daily_hour_table.date_of_checkin = daily_hour_data.get('loginDate')
            daily_hour_table.checkout = daily_hour_data.get('logoutTime')
            daily_hour_table.save()
            return Response('Success')
        else:
            return Response('Already Exists')

    if request.method == 'PUT':
        try:
            lastentried_dailyhour = employee.dailyhour_set.latest('created')
        except:
            lastentried_dailyhour = None
        if lastentried_dailyhour:
            daily_hour_data = json.loads(request.body)
            lastentried_dailyhour.checkout = daily_hour_data.get('logOutTime')
            if lastentried_dailyhour.checkin and lastentried_dailyhour.checkout:
                try:
                    checkintime = datetime.strptime(lastentried_dailyhour.checkin, '%H:%M:%S')
                    checkouttime = datetime.strptime(lastentried_dailyhour.checkout, '%H:%M:%S')
                    work_hours_today = checkouttime - checkintime
                except:
                    work_hours_today = None
                lastentried_dailyhour.hours_perday = work_hours_today if work_hours_today else None
            lastentried_dailyhour.save()
            return Response('Success')

    class DailyHourpagination(PageNumberPagination):
        page_size = 25
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    paginator = DailyHourpagination()
    employee_dailyhours = employee.dailyhour_set.all().order_by('-created')
    result_page = paginator.paginate_queryset(employee_dailyhours, request)
    serializer = DailyHourSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
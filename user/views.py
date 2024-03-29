from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import Employee,DailyHour,Leave,RemainingLeave, Holiday
from .serializers import EmployeeSerializer,LeaveSerializer,DailyHourSerializer,RemainingLeavesSerializer, PendingLeaveSerializer, AllLeaveSerializer, HolidaySerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Q
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


class GetUserRoutes(APIView):
    def get(self,request):
        routes = [
            {'GET': 'api/user/all'},
            {'GET': 'api/user/id'},
            {'GET': 'api/user/holidays'},
            {'POST': 'api/user/id'},
            {'GET': 'api/user/id/leavestatus'},
            {'POST': 'api/user/id/leavestatus'},
            {'DELETE': 'api/user/id/deleteleave'},
            {'GET': 'api/user/id/dailyhours'},
            {'POST': 'api/user/id/dailyhours'},
            {'POST': 'api/user/id/changepassword'},
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
        data['end_date_of_leave'] = leave.end_date_of_leave
        data['leave_notes'] = leave.leave_notes
        data['no_of_leaves'] = leave.no_of_leaves_required
        data['leave_type'] = leave.leave_type
        data['leave_id'] = leave.id
        data['half_day'] = leave.half_day
        pending_leaves.append(data)

    return Response(pending_leaves)


# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def getAllUsers(request):
#     class EmployeePagination(PageNumberPagination):
#         page_size = 20
#         page_size_query_param = 'page_size'
#         max_page_size = 1000
#         page_query_param = 'page'
#
#     paginator = EmployeePagination()
#     all_employees = Employee.objects.all().order_by('date_of_joining')
#     result_page = paginator.paginate_queryset(all_employees, request)
#     serializer = EmployeeSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)


class ListEmployees(APIView):

    class EmployeePagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100
        page_query_param = 'page'

    def get(self,request):
        paginator = self.EmployeePagination()
        all_employees = Employee.objects.all().order_by('date_of_joining')
        result_page = paginator.paginate_queryset(all_employees,request)
        serializer = EmployeeSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAllLeaves(request):

    class AllLeavesPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    paginator = AllLeavesPagination()
    pending_leaves = Leave.objects.filter(status=False, rejected=False).values('employee_id','employee__name','leave_type',
                    'date_of_leave', 'end_date_of_leave', 'half_day','rejected','leave_notes','leave_type','no_of_leaves_required','status','id').annotate(count=Count('employee_id'))
    result_page = paginator.paginate_queryset(pending_leaves, request)
    serializer = AllLeaveSerializer(result_page,many=True)
    total_pending_leaves = 0
    for item in pending_leaves:
        total_pending_leaves += item['count']
    context = {'data':serializer.data, 'total_pending_leaves':total_pending_leaves}
    return Response(context)


#To show the holiday
@api_view(['GET'])
def getAllHolidays(request):

    holiday_table = Holiday.objects.all().order_by('date_of_holiday')
    serializer = HolidaySerializer(holiday_table,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSearchApi(request):
    status =request.GET.get('status')
    rejected = request.GET.get('rejected')
    name = request.GET.get('name')
    leave_type = request.GET.get('leave_type')
    filter_condition = Q()
    if name and status and rejected and leave_type:

        filter_condition = (
                Q(status=status) &
                Q(leave_type=leave_type) &
                Q(employee__name__icontains=name) &
                Q(rejected=rejected)
        )
    elif name and status and rejected:
        filter_condition = (
            Q(status=status) &
            Q(employee__name__icontains=name) &
            Q(rejected=rejected)
        )
    elif name and status and leave_type:
        filter_condition = (
            Q(status=status) &
            Q(employee__name__icontains=name) &
            Q(leave_type=leave_type)
        )
    elif name  and leave_type and rejected:
        filter_condition =(
                Q(leave_type=leave_type) &
                Q(employee__name__icontains=name) &
                Q(rejected=rejected)
        )

    elif status and leave_type and rejected:
        filter_condition = (
            Q(status=status) &
            Q(leave_type=leave_type) &
            Q(rejected=rejected)
        )
    elif status and rejected:
        filter_condition = (
            Q(status=status) &
            Q(rejected=rejected)
        )
    elif leave_type and status:
        filter_condition = (
                Q(status=status) &
                Q(leave_type=leave_type)
        )
    elif leave_type and rejected:
        filter_condition = (
                Q(leave_type=leave_type) &
                Q(rejected=rejected)
        )
    elif leave_type and name:
        filter_condition = (
                Q(leave_type=leave_type) &
                Q(employee__name__icontains=name)
        )
    elif rejected and name:
        filter_condition = (
        Q(employee__name__icontains=name) &
        Q(rejected=rejected)
        )
    elif status and name:
        filter_condition = (
                Q(status=status) &
                Q(employee__name__icontains=name)
        )
    elif name:
        filter_condition = (
                Q(employee__name__icontains=name)
        )
    elif status:
        filter_condition = (
                Q(status=status)
        )
    elif rejected:
        filter_condition = (
                Q(rejected=rejected)
        )
    elif leave_type:
        filter_condition = (
                Q(leave_type=leave_type)
        )

    pending_leaves = Leave.objects.filter(status=False, rejected=False).annotate(count=Count('employee_id'))
    total_pending_leaves = len(pending_leaves)


    leaves = Leave.objects.filter(
        filter_condition
        )
    leaves_filter = []

    for leave in leaves:
        data = {}
        data['name'] = leave.employee.name
        data['employee_id'] = leave.employee.id
        data['leave_applied'] = leave.date_of_leave
        data['end_date_of_leave'] = leave.end_date_of_leave
        data['leave_notes'] = leave.leave_notes
        data['no_of_leaves'] = leave.no_of_leaves_required
        data['leave_type'] = leave.leave_type
        data['leave_id'] = leave.id
        data['half_day'] = leave.half_day
        data['rejected'] = leave.rejected
        data['status'] = leave.status
        leaves_filter.append(data)
    context = {'data':leaves_filter, 'total_pending_leaves':total_pending_leaves}
    return Response(context)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setUpdateProfile(request, id):
    # if request.method == 'PUT':
    employee = Employee.objects.get(pk=id)

    try:
        profile_data = json.loads(request.body)
    except:
        profile_data = None
    if request.FILES:
        employee.profile_image = request.FILES.get('profile_image')
        employee.save()
    if profile_data:
        for key,value in profile_data.items():
            setattr(employee,key,value)
            employee.save()
    return Response("Success")


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



# To store the applied leave by user
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getLeaves(request,id):

    employee = get_object_or_404(Employee, pk=id)

    if request.method == 'POST':
        data = request.data
        leave_table = Leave.objects.create(
            employee=employee,
            leave_type=data.get('leaveType'),
            leave_notes=data.get('leaveNotes'),
            date_of_leave=data.get('leaveDate'),
            end_date_of_leave=data.get('EndleaveDate'),
            no_of_leaves_required=data.get('noOfLeaves'),
            half_day=data.get('half_day')
        )

        return Response("Success")

    employee_leaves = Leave.objects.filter(employee=employee)
    serializer = LeaveSerializer(employee_leaves, many=True)
    return Response(serializer.data)


# edit leave table by admin
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def setLeaveTable(request,id):
    # if request.method == 'PUT':
    employee = Employee.objects.get(pk=id)
    remaining_leaves = RemainingLeave.objects.get(employee=employee)
    # except output in this format
    # [{"no_of_leaves": 1, "leave_type": 4}, {"no_of_leaves": 1, "leave_type": 3},{"no_of_leaves": 1, "leave_type": 2},
    # {"no_of_leaves": 1, "leave_type": 1},{"no_of_leaves": 1, "leave_type": 5}]
    try:
        leave_table_data = json.loads(request.body)
    except:
        leave_table_data = None
    for data in leave_table_data:
        leavetype = data.get('leave_type')
        if leavetype == 1:
            remaining_leaves.casual_leave = data.get('no_of_leaves')
        elif leavetype == 2:
            remaining_leaves.sick_leave = data.get('no_of_leaves')
        elif leavetype == 3:
            remaining_leaves.emergency_leave = data.get('no_of_leaves')
        elif leavetype == 4:
            remaining_leaves.comp_off = data.get('no_of_leaves')
        elif leavetype == 5:
            remaining_leaves.optional_holidays = data.get('no_of_leaves')

        remaining_leaves.save()

    return Response("Success")


#get remaining leaves of each employee
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
    employee_leave = get_object_or_404(Leave, pk=id)
    status = request.data.get('leavestatus', None)
    attribute_map = {
        'Pending': {},
        'Approved': {'status': True},
        'Rejected': {'rejected': True}
    }
    try:
        updates = attribute_map.get(status, {})
        for attr, value in updates.items():
            setattr(employee_leave, attr, value)
        employee_leave.save()
    except Exception as e:
        return Response("Failed Approving Leave -> {}".format(e))
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
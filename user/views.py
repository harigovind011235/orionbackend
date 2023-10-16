import django_filters
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,ListCreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework import status
from .models import Employee,DailyHour,Leave,RemainingLeave, Holiday
from .serializers import EmployeeSerializer,LeaveSerializer,DailyHourSerializer,RemainingLeavesSerializer, PendingLeaveSerializer, AllLeaveSerializer, HolidaySerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime



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

    @method_decorator(cache_page(60*1))
    def get(self, request):
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


class ListRetrieveUpdateEmployees(CreateModelMixin,ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericAPIView):

    class EmployeePagination(PageNumberPagination):
        page_size = 2
        page_size_query_param = 'page_size'
        max_page_size = 100
        page_query_param = 'page'

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination

    @method_decorator(cache_page(60 * 2))
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)


    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message":"Employee Created Successfully"},status=status.HTTP_201_CREATED,headers=headers)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def update(self, request, *args, **kwargs):
        employee_instance = self.get_object()
        serializer = self.get_serializer(instance=employee_instance,data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"message":"Employee Updated Successfully"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message":"Employee Deleted Successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"Not Deleted","error":e})


class AllLeavesListView(ListAPIView):

    class AllLeavesPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    serializer_class = AllLeaveSerializer
    pagination_class = AllLeavesPagination

    def get_queryset(self):
        pending_leaves = Leave.objects.filter(status=False, rejected=False).values('employee_id', 'employee__name',
         'leave_type','date_of_leave', 'end_date_of_leave','half_day', 'rejected','leave_notes', 'leave_type',
         'no_of_leaves_required', 'status','id')
        return pending_leaves

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)

        total_pending_leaves = len(list(queryset))
        context = {'data': serializer.data, 'total_pending_leaves': total_pending_leaves}
        return Response(context)


class GetIndividualEmployeeLeaves(ListAPIView):
    serializer_class = LeaveSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        try:
            employee = Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            employee = None
        return employee

    def list(self, request, *args, **kwargs):
        employee = self.get_queryset()
        if not employee:
            return Response({"message":"Employee Does Not Exists"},status=status.HTTP_404_NOT_FOUND)
        pending_leaves = employee.leave_set.filter(status=False,rejected=False)
        serializer = self.serializer_class(pending_leaves,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetCreateUpdateDeleteHolidays(ListModelMixin,RetrieveModelMixin,CreateModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):

    class HolidaysPagination(PageNumberPagination):
        page_size = 2
        page_size_query_param = 'page_size'
        max_page_size = 100
        page_query_param = 'page'

    queryset = Holiday.objects.all().order_by('date_of_holiday')
    serializer_class = HolidaySerializer
    pagination_class = HolidaysPagination

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Holiday Created Successfully"}, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        employee_instance = self.get_object()
        serializer = self.get_serializer(instance=employee_instance, data=request.data,partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"message": "Holiday Updated Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Holiday Deleted Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Not Deleted", "error": e})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,id,format=None):
        employee = get_object_or_404(Employee,pk=id)
        user = employee.user

        try:
            new_password_data = request.data
        except:
            new_password_data = None

        if new_password_data:
            current_password = new_password_data.get('current_password')
            new_password = new_password_data.get('new_password')

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response({"Message":"Password Changed Successfully"})


class GetCreateEmployeeLeaves(APIView):
    # permission_classes = [IsAuthenticated]

    def get_employee(self):
        return get_object_or_404(Employee, pk=self.kwargs['id'])

    def get(self,request,id,format=None):
        employee = self.get_employee()
        employee_leaves = Leave.objects.filter(employee=employee)
        serializer = LeaveSerializer(employee_leaves,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,id,format=None):
        employee = self.get_employee()
        data = request.data
        leave_instance = Leave.objects.create(
            employee=employee,
            leave_type=data.get('leaveType'),
            leave_notes=data.get('leaveNotes'),
            date_of_leave=data.get('leaveDate'),
            end_date_of_leave=data.get('EndleaveDate'),
            no_of_leaves_required=data.get('noOfLeaves'),
            half_day=data.get('half_day')
        )
        return Response("Leave Applied Successfully",status=status.HTTP_201_CREATED)


class UpdateLeaveStatusAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,id,format=None):
        employee = get_object_or_404(Employee,pk=id)
        remaining_leaves = RemainingLeave.objects.get(employee=employee)

        try:
            leave_table_data = request.data
        except:
            leave_table_data = None

        if leave_table_data:
            changes = {}
            for data in leave_table_data:
                leavetype = data.get('leave_type')
                if leavetype == 1:
                    changes['casual_leave'] = data.get('no_of_leaves')
                elif leavetype == 2:
                    changes['sick_leave'] = data.get('no_of_leaves')
                elif leavetype == 3:
                    changes['emergency_leave'] = data.get('no_of_leaves')
                elif leavetype == 4:
                    changes['comp_off'] = data.get('no_of_leaves')
                elif leavetype == 5:
                    changes['optional_holidays'] = data.get('no_of_leaves')

            for field,value in changes.items():
                setattr(remaining_leaves,field,value)

            remaining_leaves.save()

            return Response({"message":"Leave Updated Successfully"},status=status.HTTP_200_OK)
        else:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class RemainingLeavesDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemainingLeavesSerializer

    def get_object(self):
        employee = get_object_or_404(Employee,pk=self.kwargs['id'])
        return get_object_or_404(RemainingLeave,employee=employee)


class LeaveUpdateView(UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RemainingLeavesSerializer

    def update(self,request,*args,**kwargs):
        employee_leave = self.get_object()
        status = request.data.get('leavestatus',None)
        attribute_map = {
            'Pending':{},
            'Approved':{'status':True},
            'Rejected':{'rejected':True}
        }
        try:
            updates = attribute_map.get(status,{})
            for field,value in updates.items():
                setattr(employee_leave,field,value)

            employee_leave.save()
        except Exception as e:
            return Response(f"Failed Approving Leave -> {e}")

        return Response({"message":"Update Leave Successfully"},status=status.HTTP_200_OK)


class LeaveDeleteView(DestroyAPIView):
    queryset = Leave.objects.all()

    def destroy(self, request, *args, **kwargs):
        current_leave = self.get_object()
        if current_leave.status == False:
            current_leave.delete()
            return Response({"Message":"Deleted One Leave"},status=status.HTTP_200_OK)
        else:
            return Response("Already Approved")


class DailyHourView(ListCreateAPIView):

    class DailyHourpagination(PageNumberPagination):
        page_size = 25
        page_size_query_param = 'page_size'
        max_page_size = 1000
        page_query_param = 'page'

    permission_classes = [IsAuthenticated]
    serializer_class = DailyHourSerializer
    pagination_class = DailyHourpagination

    def get_queryset(self):
        employee = get_object_or_404(Employee,pk=self.kwargs['id'])
        return employee.dailyhour_set.all().order_by('-created')

    def create(self,request,*args,**kwargs):
        employee = get_object_or_404(Employee,pk=self.kwargs['id'])
        today = timezone.localtime().date()
        entry_exists = DailyHour.objects.filter(created__date=today,employee=employee).exists()

        if not entry_exists:
            daily_hour_data = request.data
            daily_hour_table = DailyHour.objects.create(
                employee=employee,
                checkin=daily_hour_data.get('loginTime'),
                date_of_checkin=daily_hour_data.get('loginDate'),
                checkout=daily_hour_data.get('logoutTime')
            )
            return Response('Success', status=status.HTTP_201_CREATED)


class DailyHourDetailView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DailyHour.objects.all()
    serializer_class = DailyHourSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        lastentried_dailyhour = instance

        if lastentried_dailyhour:
            daily_hour_data = request.data
            lastentried_dailyhour.checkout = daily_hour_data.get('logOutTime')

            if lastentried_dailyhour.checkin and lastentried_dailyhour.checkout:
                try:
                    checkintime = datetime.strptime(lastentried_dailyhour.checkin,'%H:%M:%S')
                    checkouttime = datetime.strptime(lastentried_dailyhour.checkout,'%H:%M:%S')
                    work_hours_today = checkouttime - checkintime
                except:
                    work_hours_today = None

                lastentried_dailyhour.hours_perday = work_hours_today if work_hours_today else None
                lastentried_dailyhour.save()
                return Response('Success')


class EmployeesLeaveSearchView(ListAPIView):

    class LeaveFilter(filters.FilterSet):
        name = django_filters.CharFilter(field_name='employee__name',lookup_expr='icontains')
        status = django_filters.BooleanFilter()
        rejected = django_filters.BooleanFilter()
        half_day = django_filters.BooleanFilter()
        leave_type = django_filters.CharFilter()
        class Meta:
            model = Leave
            fields = ['name','status','rejected','half_day','leave_type']

    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = LeaveFilter


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


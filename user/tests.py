from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee,Holiday,Leave  # Import your Employee model
from .serializers import EmployeeSerializer,HolidaySerializer,LeaveSerializer  # Import your EmployeeSerializer


class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        # Create a sample employee instance for testing
        self.employee_data = {
            'employee_id': 'EMP123',
            'name': 'John Doe',
            'email': 'john@example.com',
            'bio': 'A software engineer with a passion for coding.',
            'username': 'johndoe',
            'location': 'New York',
            'contact_no': '1234567890',
            'alternate_contact': '9876543210',
            'blood_group': 'AB+',
            'designation': 'Senior Developer',
            'date_of_joining': '2022-01-15',
            'dob': '1990-05-25',
            'status': True,
        }
        self.employee = Employee.objects.create(**self.employee_data)

        # Define the API URL
        self.list_url = reverse('list-employees')
        self.detail_url = reverse('get-employee', kwargs={'pk': self.employee.pk}) # Change 'employees' to your URL name


    def test_list_employees(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        actual_data = response.data.get('results',[])
        expected_data = EmployeeSerializer(Employee.objects.all(), many=True).data
        self.assertEqual(actual_data, expected_data)


    def test_retrieve_employee(self):
        detail_url = reverse('get-employee', kwargs={'pk': self.employee.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = EmployeeSerializer(self.employee).data
        self.assertEqual(response.data, expected_data)


    def test_create_employee(self):
        new_employee_data = {
            'employee_id': 'EMP123',
            'name': 'Saranya bs',
            'email': 'saranya@example.com',
            'bio': 'A software engineer with a passion for coding.',
            'username': 'saranaa',
            'location': 'tvm',
            'contact_no': '9393948293',
            'alternate_contact': '9876543210',
            'blood_group': 'AB+',
            'designation': 'Senior Developer',
            'date_of_joining': '2022-01-15',
            'dob': '1990-05-25',
            'status': True,
        }
        response = self.client.post(self.list_url, new_employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_employee(self):
        update_data = {
            'username': 'harigovind',
            'email':"harigovind@gmail.com"
        }
        detail_url = reverse('get-employee', kwargs={'pk': self.employee.pk})
        response = self.client.put(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_employee(self):
        try:
            detail_url = reverse('get-employee', kwargs={'pk': self.employee.pk})
            response = self.client.delete(detail_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            print("Delete failed -> {}".format(e))


class HolidayAPITestCases(APITestCase):

    def setUp(self):
        self.holiday_data = {
            'date_of_holiday': '2023-12-25',  # Date in yyyy-mm-dd format
            'event': 'Christmas',
            'region_applicable': 'Global',
            'optional_holiday': False,
        }

        self.holiday = Holiday.objects.create(**self.holiday_data)
        self.list_url = reverse('get-create-holidays')
        self.detail_url = reverse('get-update-delete-holidays',kwargs={'pk':self.holiday.pk})


    def test_list_holidays(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        actual_data = response.data.get('results',[])
        expected_data = HolidaySerializer(Holiday.objects.all(),many=True).data
        self.assertEqual(actual_data,expected_data)


    def test_create_holidays(self):
        response = self.client.post(self.list_url,self.holiday_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_update_holiday(self):
        updated_data = {
            'event': 'New Year',
            'region_applicable': 'Local',
            'optional_holiday': True,
        }
        response = self.client.put(self.detail_url,updated_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'),"Holiday Updated Successfully")


    def test_delete_holiday(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertFalse(Holiday.objects.filter(pk=self.holiday.pk).exists())


class LeavesActionsTestCases(APITestCase):
    def test_list_leaves(self):
        list_url = reverse('all_leaves')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        instance = Leave.objects.filter(status=False, rejected=False).values('employee_id', 'employee__name',
         'leave_type','date_of_leave', 'end_date_of_leave','half_day', 'rejected','leave_notes', 'leave_type',
         'no_of_leaves_required', 'status','id')
        expected_data = LeaveSerializer(instance,many=True).data
        actual_data = response.data.get('data')
        self.assertEqual(actual_data,expected_data)

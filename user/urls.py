
from django.urls import path
from . import views


urlpatterns = [
    # path('all-leave-requests',views.getAllPendingLeaves,name="allpendingleaves"),
    # path('<str:id>/updateprofile',views.setUpdateProfile,name="updateprofile"),
    # path('searchapi', views.getSearchApi, name="searchapi"),
    path('routes', views.GetUserRoutes.as_view(), name="user-routes"),
    path('all-leaves/', views.AllLeavesListView.as_view(), name='all_leaves'),
    path('holidays', views.GetCreateUpdateDeleteHolidays.as_view(), name='get-create-holidays'),
    path('holidays/<str:pk>/', views.GetCreateUpdateDeleteHolidays.as_view(), name='get-update-delete-holidays'),
    path('leave-search', views.EmployeesLeaveSearchView.as_view(), name="leave-search"),
    path('<str:id>/employee-pending-leaves',views.GetIndividualEmployeeLeaves.as_view(),name="remainingleaveapprovals"),
    path('<str:id>/update-leave',views.LeaveUpdateView.as_view(),name="updateleave"),
    path('',views.ListRetrieveUpdateEmployees.as_view(),name="list-employees"),
    path('<uuid:pk>/',views.ListRetrieveUpdateEmployees.as_view(),name="get-employee"),
    path('<str:id>/leavestatus',views.GetCreateEmployeeLeaves.as_view(),name="leaves"),
    path('<str:id>/deleteleave',views.LeaveDeleteView.as_view(),name="deleteleaves"),
    path('<str:id>/leavetable', views.UpdateLeaveStatusAdmin.as_view(), name="leavetable"),
    path('<str:id>/remainingleaves',views.RemainingLeavesDetailView.as_view(),name="remainingleaves"),
    path('<str:id>/dailyhours',views.DailyHourView.as_view(),name="list-create-dailyhours"),
    path('<str:id>/dailyhours/update',views.DailyHourDetailView.as_view(),name="update-dailyhours"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:id>/changepassword', views.ChangePassword.as_view(), name="changepassword"),
]
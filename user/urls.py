
from django.urls import path
from . import views


urlpatterns = [
    path('routes',views.getUserRoutes,name="user-routes"),
    path('all-leave-requests',views.getAllPendingLeaves,name="allpendingleaves"),
    path('<str:id>/employee-pending-leaves',views.getLeavesForApproval,name="remainingleaveapprovals"),
    path('<str:id>/update-leave',views.updateEmployeeLeave,name="updateleave"),
    path('all',views.getAllUsers,name="allusers"),
    path('<str:id>',views.getProfile,name="profile"),
    path('<str:id>/updateprofile',views.setUpdateProfile,name="updateprofile"),
    path('<str:id>/leavestatus',views.getLeaves,name="leaves"),
    path('<str:id>/deleteleave',views.leavesDelete,name="deleteleaves"),
    path('<str:id>/leavetable', views.setLeaveTable, name="leavetable"),
    path('<str:id>/remainingleaves',views.getRemainingLeaves,name="remainingleaves"),
    path('<str:id>/dailyhours',views.getDailyHours,name="dailyhours"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:id>/changepassword', views.setChangePassword, name="changepassword"),
]
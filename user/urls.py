
from django.urls import path
from . import views


urlpatterns = [
    path('routes',views.getUserRoutes,name="user-routes"),
    path('all-leave-requests',views.getAllPendingLeaves,name="allpendingleaves"),
    path('all',views.getAllUsers,name="allusers"),
    path('<str:id>',views.getProfile,name="profile"),
    path('<str:id>/leavestatus',views.getLeaves,name="leaves"),
    path('<str:id>/deleteleave',views.leavesDelete,name="deleteleaves"),
    path('<str:id>/remainingleaves',views.getRemainingLeaves,name="remainingleaves"),
    path('<str:id>/dailyhours',views.getDailyHours,name="dailyhours"),
    path('<str:id>/leave-requests',views.getLeaveRequest,name="leaverequest"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('<str:id>/changepassword', views.setChangePassword, name="changepassword"),
]
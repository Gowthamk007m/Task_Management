from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, AdminTaskViewSet, 
    UserTaskListView, UserTaskUpdateView, TaskReportView
)
from django.contrib.auth import views as auth_views
# Import renamed views file
from . import template_views

# Router for viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'admin/tasks', AdminTaskViewSet)

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API routes
    path('', include(router.urls)),
    
    # User API endpoints
    path('tasks/', UserTaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', UserTaskUpdateView.as_view(), name='update-task'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task-report'),
    
    # Template views for traditional Django rendering
    path('dashboard/', template_views.home, name='home'),
    path('users/', template_views.user_list, name='user_list'),
    path('users/<int:pk>/', template_views.user_detail, name='user_detail'),
    path('tasks/list/', template_views.task_list, name='task_list'),
    path('tasks/detail/<int:pk>/', template_views.task_detail, name='task_detail'),
    path('tasks/create/', template_views.task_create, name='task_create'),
    path('tasks/update/<int:pk>/', template_views.task_update, name='task_update'),
    path('tasks/report/<int:pk>/', template_views.task_report, name='task_report'),


    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
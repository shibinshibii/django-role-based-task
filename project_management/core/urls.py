from django.urls import path
from .views import RoleManagementView, UserManagementView, EmployeeCreateView, ProjectManagmentView, TaskManagementView, TaskStatusUpdateView, CurrentUserView, ChangePasswordView, ForgotPasswordView, ResetPasswordView


urlpatterns = [
    path("roles/", RoleManagementView.as_view()),
    path('users/', UserManagementView.as_view()),
    path('employees/', EmployeeCreateView.as_view()),
    path('projects/', ProjectManagmentView.as_view()),
    path('tasks/', TaskManagementView.as_view()),
    path('tasks/<int:pk>/', TaskStatusUpdateView.as_view()),
    path('user/', CurrentUserView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

]

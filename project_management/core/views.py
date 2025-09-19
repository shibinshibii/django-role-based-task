from django.shortcuts import render
from .models import CustomUser, Project, Role, Task
from .serializers import RoleSerializer, ProjectSerializer, TaskSerializer, UserSerializer, CurrentUserSerializer,AdminCreateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.throttling import AnonRateThrottle

class AdminCreateView(APIView):
    def post(self,request):
        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors)
class RoleManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        if not user.role or user.role.name.lower() != "admin":
            return Response({"detail": "You do not have permission to create roles"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.role or user.role.name.lower() != "admin":
            return Response({"detail": "Only admin can view all users"}, status=status.HTTP_403_FORBIDDEN)
        all_users = CustomUser.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        email = request.data.get("email")
        username = request.data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail": "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "E-mail already in use"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.role or user.role.name.lower() != "admin":
            return Response({"detail": "Only admin can create Coordinators"}, status=status.HTTP_403_FORBIDDEN)
        role_name = request.data.get("creatingUserRole")
        if not role_name or role_name.lower() != "project coordinator":
            return Response({"detail": "The role must be Project Coordinator"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role_obj = Role.objects.get(name__iexact="Project Coordinator")

        except Role.DoesNotExist:
            return Response({"detail": "Role does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data={**request.data, "role": role_obj.id})
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "User created successfully. Credentials sent to email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class EmployeeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        email = request.data.get("email")
        username = request.data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail": "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "E-mail already in use"}, status=status.HTTP_400_BAD_REQUEST)
        allowed_roles = ["project coordinator", "admin"]
        if not user.role or user.role.name.lower() not in allowed_roles:
            return Response({"detail": "You don't have permission to create employees"}, status=status.HTTP_403_FORBIDDEN)
        role_name = request.data.get("creatingUserRole")
        if not role_name or role_name.lower() != "employee":
            return Response({"detail": "The role must be Employee"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role_obj = Role.objects.get(name__iexact="Employee")

        except Role.DoesNotExist:
            return Response({"detail": "Role does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data={**request.data, "role": role_obj.id})
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "User created successfully. Credentials sent to email."}, status=201)
        return Response(serializer.errors, status=400)


class ProjectManagmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        

        allowed_roles = ["project coordinator", "admin"]
        if not user.role or user.role.name.lower() not in allowed_roles:
            return Response({"detail": "You dont have permission to create projects"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        projects = Project.objects.filter(created_by=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        allowed_roles = ["project coordinator", "admin"]
        if not user.role or user.role.name.lower() not in allowed_roles:
            return Response({"detail": "You don't have permission to assign tasks"},
                            status=status.HTTP_403_FORBIDDEN)

        assigned_to_id = request.data.get('assigned_to')

        try:
            employee = CustomUser.objects.get(id=assigned_to_id)
            print(employee)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Assigned user does not exist"}, status=400)
        if not employee.role or employee.role.name.lower() != "employee":
            print(employee.role, employee.role.name)
            return Response({"detail": "Tasks can be only assigned to employees"})

        project_id = request.data.get("project")

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"detail": "Project does not exist"}, status=400)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    def get(self, request):
        user = request.user

        if not user.role or user.role.name.lower() != "employee":
            return Response({"detail": "Only employees have tasks"},
                            status=status.HTTP_403_FORBIDDEN)
        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"detail": "No such task"}, status=400)

        user = request.user

        if user.role.name.lower() == "employee":
            if task.assigned_to != user:
                return Response({"detail": "You can only update your own tasks"}, status=400)

        new_status = request.data.get("status")

        if not new_status:
            return Response({"detail": "Status required"})
        valid_status = [choice[0] for choice in Task.status_choices]

        if new_status not in valid_status:
            return Response({"detail": "Invalid status"}, status=400)

        task.status = new_status
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        serializer = CurrentUserSerializer(user)
        return Response(serializer.data, status=200)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")
        confirm_password = request.data.get("confirmPassword")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=403)

        if confirm_password != new_password:
            return Response({"detail": "Passwords do not match"}, status=400)

        if old_password == new_password:
            return Response({"detail": "New password cannot be the same as the old password"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password Changed Successfully, Redirecting to Login..."}, status=200)


class ForgotPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = []  

    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "No user with this email."}, status=404)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:5173/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response({"detail": "Password reset link sent to email."}, status=200)


class ResetPasswordView(APIView):
    permission_classes = []  # No auth required

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("newPassword")
        confirm_password = request.data.get("confirmPassword")
        if new_password != confirm_password:
            return Response({"detail":"The passwords do not match"})
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid user."}, status=400)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password reset successfull. Redirecting to Login..."}, status=200)

from django.shortcuts import render
from .models import CustomUser,Project,Role,Task
from .serializers import RoleSerializer,ProjectSerializer,TaskSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



class RoleManagementView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        user = request.user

        if not user.role or user.role.name.lower() != "admin":
            return Response({"detail": "You do not have permission to create roles"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserManagementView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        if not user.role or user.role.name.lower() != "admin":    
            return Response({"detail":"Only admin can view all users"},status=status.HTTP_403_FORBIDDEN)
        all_users = CustomUser.objects.all()
        serializer = UserSerializer(all_users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        user = request.user
        if not user.role or user.role.name.lower() != "admin":
            return Response({"detail":"Only admin can create Coordinators"},status=status.HTTP_403_FORBIDDEN)
        role_name = request.data.get("role")
        if not role_name or role_name.lower() != "project coordinator":
            return Response({"detail":"The role must be Project Coordinator"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role_obj = Role.objects.get(name__iexact="Project Coordinator")

        except Role.DoesNotExist:
            return Response({"detail":"Role does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = UserSerializer(data={**request.data, "role": role_obj.id})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EmployeeCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user = request.user
        if not user.role or user.role.name.lower() != "project coordinator":
            return Response({"detail":"Only Project Coordinators can create Employees"},status=status.HTTP_403_FORBIDDEN)
        role_name = request.data.get("role")
        if not role_name or role_name.lower() != "employee":
            return Response({"detail":"The role must be Employee"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role_obj = Role.objects.get(name__iexact="Employee")

        except Role.DoesNotExist:
            return Response({"detail":"Role does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data={**request.data, "role": role_obj.id})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
class ProjectManagmentView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user = request.user

        if not user.role or user.role.name.lower() != 'project coordinator':
            return Response({"detail":"Only Project Coordinators can create Projects.."},status=status.HTTP_403_FORBIDDEN)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        projects = Project.objects.filter(created_by=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskManagementView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        if not user.role or user.role.name.lower() != "project coordinator":
            return Response({"detail": "Only Project Coordinators can assign tasks"},
                            status=status.HTTP_403_FORBIDDEN)
        
        assigned_to_id = request.data.get('assigned_to')

        try:
            employee = CustomUser.objects.get(id=assigned_to_id)
            print(employee)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Assigned user does not exist"}, status=400)
        if not employee.role or employee.role.name.lower() != "employee":
            print(employee.role,employee.role.name)
            return Response({"detail":"Tasks can be only assigned to employees"})
        
        project_id = request.data.get("project")

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"detail":"Project does not exist"},status=400)
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)

    def get(self,request):
        user = request.user

        if not user.role or user.role.name.lower() != "employee":
            return Response({"detail": "Only employees can view their tasks"},
                            status=status.HTTP_403_FORBIDDEN)
        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self,request,pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"detail":"No such task"},status=400)
        
        user = request.user

        if user.role.name.lower() == "employee":
            if task.assigned_to != user:
                return Response({"detail":"You can only update your own tasks"},status=400)
        
        new_status = request.data.get("status")

        if not new_status:
            return Response({"detail":"Status required"})
        valid_status = [choice[0] for choice in Task.status_choices]

        if new_status not in valid_status:
            return Response({"detail":"Invalid status"},status=400)
        
        task.status = new_status
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)




        


        


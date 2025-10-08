from rest_framework import serializers
from django.conf import settings
from .models import CustomUser, Role, Project, Task
from django.core.mail import send_mail
import random
import string
import threading


class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "role")

    def create(self, validated_data):
        admin_role = Role.objects.get(name="Admin")
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            role=admin_role,
            email=validated_data['email'],
            password=validated_data['password']


        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "role", "email")
        # extra_kwargs = {'password':{"write_only":True}}

    def create(self, validated_data):
        password = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10))
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            role=validated_data['role'],
            email=validated_data['email'],
            password=password
        )

        # send email with credentials in background thread
        def send_email_async():
            send_mail(
                subject="Your new account credentials",
                message=f"Hello {user.username},\n\n"
                        f"Your account has been created.\n"
                        f"Username: {user.username}\nPassword: {password}\n\n"
                        "Please login and change your password.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )

        threading.Thread(target=send_email_async).start()
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "role_name")


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

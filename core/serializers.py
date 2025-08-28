from rest_framework import serializers
from .models import CustomUser,Role,Project,Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username",'password',"role")
        extra_kwargs = {'password':{"write_only":True}}

        def create(self,validated_data):
            password = validated_data.pop("password")
            user = CustomUser(**validated_data)
            user.set_password(password)
            user.save()
            return user

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



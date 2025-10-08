from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True,related_name='users')

    def __str__(self):
        return self.username
    
class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    assigned_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status_choices = [
        ("PENDING","PENDING"),
        ('IN_PROGRESS','IN_PROGRESS'),
        ('DONE','DONE')
    ]
    status = models.CharField(choices=status_choices,max_length=50,default="PENDING")
    def __str__(self):
        return self.title





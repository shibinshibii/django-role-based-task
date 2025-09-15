from django.contrib import admin
from .models import Role,CustomUser,Task,Project

# Register your models here.
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Project)


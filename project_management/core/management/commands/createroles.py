
from django.core.management.base import BaseCommand
from core.models import Role

class Command(BaseCommand):
    help = "Creates default roles (Admin, Project Coordinator, Employee)"

    def handle(self, *args, **kwargs):
        roles = ["Admin", "Project Coordinator", "Employee"]
        for r in roles:
            role, created = Role.objects.get_or_create(name=r)
            if created:
                print(f"Role '{r}' created")
            else:
                print(f"Role '{r}' already exists")

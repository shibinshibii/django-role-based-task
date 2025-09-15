**Set-up**

- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

**Test using Postman or any other provider**

*Authentication:*
- POST /api/token/ → Get JWT tokens
- POST /api/token/refresh/ → Refresh token

*Role Management:*
- POST /roles/ → Admin creates a new role
- GET /roles/ → View all roles

*User Management:*
- POST /users/ → Admin creates Coordinators
- POST /employees/ → Coordinator creates Employees
- GET /users/ → Admin views all users

*Project Management:*
- POST /projects/ → Coordinator creates Project
- GET /projects/ → Coordinator views their Projects

*Task Management:*
- POST /tasks/ → Coordinator assigns Task to Employee
- GET /tasks/ → Employees view their Tasks
- PATCH /tasks/{id}/ → Employee updates Task status

--you can test using postman or any other service providers.


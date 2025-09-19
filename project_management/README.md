**The backend made using Django Rest Framework**

**Set-up**

- python -m venv venv - create a virtual environment
- venv\Scripts\activate - activate the environment
- pip install -r requirements.txt - install the requirements after activating the environment variable
- python manage.py makemigrations - make migrations
- python manage.py migrate
- python manage.py runserver - run the server

**Setting up the email-provider**

- create a .env file and add these values 
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"          
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "" 
    EMAIL_HOST_PASSWORD = ""  
    DEFAULT_FROM_EMAIL = ""

**Test using Postman or any other provider**

*Authentication:*
- POST /api/token/ → Get JWT tokens
- POST /api/token/refresh/ → Refresh token

*Role Management:*
- POST /roles/ → Admin creates a new role
- GET /roles/ → View all roles

*User Management:*
- GET /user/ → Gets the current logged in user
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

*Password Reset Management*
- POST /change-password/ → Change password using old password
- POST /forgot-password/ → Reset password using email. Sends uid and token to the /reset-password/ endpoint.
- POST /reset-password/ → Accept token and uid and new password and changes it.

--you can test using postman or any other service providers.


**The backend made using Django Rest Framework**

**Set-up**

- `python -m venv venv` - create a virtual environment
- venv\Scripts\activate - activate the environment
- pip install -r requirements.txt - install the requirements after activating the environment variable
- python manage.py makemigrations - make migrations
- python manage.py migrate
- python manage.py runserver

**Creating Roles**

- run `python manage.py createroles` to create roles. 
- if you want to add or change the roles go to core/management/commands/createroles.py

**Creating the Admin**

- You need an admin to create coordinators and employees(Note that you need to create the roles before creating admin).
- Go to /create-admin/ endpoint using Postman.
- ```json {"username":"admin_username","email":"admin_email","password":"admin_password"}```
- Add this inside the body section(change the values).
- RUN , Admin will be created.
-

**Setting up the email-provider**

- create a .env file
- add values refering to .env.sample file.



**Test using Postman or any other provider**

_Authentication:_

- POST /api/token/ → Get JWT tokens
- POST /api/token/refresh/ → Refresh token

_Role Management:_

- POST /roles/ → Admin creates a new role
- GET /roles/ → View all roles

_User Management:_

- GET /user/ → Gets the current logged in user
- POST /users/ → Admin creates Coordinators
- POST /employees/ → Coordinator creates Employees
- GET /users/ → Admin views all users

_Project Management:_

- POST /projects/ → Coordinator creates Project
- GET /projects/ → Coordinator views their Projects

_Task Management:_

- POST /tasks/ → Coordinator assigns Task to Employee
- GET /tasks/ → Employees view their Tasks
- PATCH /tasks/{id}/ → Employee updates Task status

_Password Reset Management_

- POST /change-password/ → Change password using old password
- POST /forgot-password/ → Reset password using email. Sends uid and token to the /reset-password/ endpoint.
- POST /reset-password/ → Accept token and uid and new password and changes it.

--you can test using postman or any other service providers.

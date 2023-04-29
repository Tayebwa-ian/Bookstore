Pre-requisites:
    -python 3.11
    -Mysql server(lastest version)

To run this project use these steps for guidance
    1. Preferably create a folder on your local machine
    2. Create a virtual environment to isolate our package dependencies locally
    3. install all the dependencies from the requirements.txt file 
       with the command "pip install -r requirements.txt"
    4. install and run mysql server on your machine
    5. set environment varialables like secret key and database access credentials
    6. run database migrations with these two commands
       -python manage.py makemigrations
       -python manage.py migrate
    7. finally use the command "python manage.py runserver" to start the server

Running automated tests:
A few automated tests have been implemented due to time constraint
use the command "python manage.py test" to run them.

Postman publication can be accessed via the link below:
https://documenter.getpostman.com/view/25438703/2s93eSZb25
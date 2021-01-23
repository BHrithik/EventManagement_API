# EventManagement_API

To run this API Follow the commands

Navigate to the downloaded folder using terminal and follow these commands

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser (Create a super user)

python manage.py runserver


We can use the link http://127.0.0.1:8000/signup/        - to register as a user and you will recieve a token in return for further authentication

We can use the link http://127.0.0.1:8000/login/         - to sign in and recieve the token once again if you forget the token

We can use the link http://127.0.0.1:8000/event/         - (GET/POST) to either create an event or to look at all the events

We can use the link http://127.0.0.1:8000/event/<pk>     - (GET/PUT/DELETE)where pk is the unique id of a particular event for further details

We can use the link http://127.0.0.1:8000/users/         - (GET/POST) to either sign yourself for a particular event or to see which users are attending which event (note a user cannot regiter for more than 3 events )

We can use the link http://127.0.0.1:8000/users/<pk>     - (GET/PUT/DELETE)where pk is the unique id of a particular user for further details

We can use the link http://127.0.0.1:8000/event_user/<pk>- (GET) to get the list of all the events a single user is attending when provided his id

from django.urls import path
from .views import SignUpView,event_list,event_details,users_list,user_details,single_event
from rest_framework.authtoken.views import obtain_auth_token
app_name="eventm"

urlpatterns = [ 
path('signup/',SignUpView,name="signup"),
path('login/',obtain_auth_token,name="login"),
path('event/',event_list),
path('event/<pk>',event_details),
path('users/',users_list),
path('user/<pk>',user_details),
path('event_user/<pk>',single_event),
]
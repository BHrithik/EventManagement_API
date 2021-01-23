from rest_framework import serializers
from .models import Account,User,Event

class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Account
        fields = ['email','username','password','password2']
        extra_kwargs = { 
            'password':{'write_only':True}
        }
    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            )   
        password  = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password":"Passwords do not match!"})
        account.Password=password
        account.save()
        return account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID','userName','email','userEvents']  

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventID','eventName','eventLocation','date','eventVacancies']

class SingleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID','userName','email']

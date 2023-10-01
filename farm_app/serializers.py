from rest_framework import serializers
from .models import *
# from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email','password','first_name','last_name','phone','role_type','profile_photo']

    def validate_profile_photo(self, value):

        return value  


class VerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)



class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
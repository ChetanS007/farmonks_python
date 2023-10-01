from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import *
from .email_veri import *
import uuid
from django.http import HttpResponse
from django.views import View
from django.core.cache import cache
from django.contrib.auth import authenticate,logout,login
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class VerifyEmail(APIView):

    
    @swagger_auto_schema(
    responses={200: 'OK', 401: 'Unauthorized'},
    )
    def get(self, request,token,*args, **kwargs):

        try:

            user =User.objects.get(email_token=token)
            user.save()
            return Response({"message": "Email verification done"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Invalid Token.")

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['otp'],
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp'),
                
            },
            )
        )

    def post(self, request,token,*args, **kwargs):
        try:
            serializer = VerificationSerializer(data=request.data)
            print('serializer',serializer)
            if serializer.is_valid():
               
                OTP = cache.get("OTP")
                if serializer.validated_data['otp'] == OTP:
                # OTP is correct
                    user =User.objects.get(email_token=token)
                    user.is_verified = True
                    user.save()
                    return Response({"message": "verification done"}, status=status.HTTP_200_OK)
                else:
                # OTP is incorrect
                    return Response({"message": "OTP is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            return Response("Invalid Token.")                
        except Exception as e:
            return Response("Invalid Token.")


class RegisterUser(APIView):
    try:

        @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password','role_type','phone'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last_name'),
                'role_type': openapi.Schema(type=openapi.TYPE_STRING, description='User role'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='User phone'),
            },
            )
        )
        def post(self,request,*args,**kwargs,):

            try:
                serializer_obj = RegisterSerializer(data=request.data)
                
                if serializer_obj.is_valid():
                    ''' here serializer validate our request data create and store into db'''
                    serializer_obj.save()
                    email_token = str(uuid.uuid4())
                    send_email_to_user(request,serializer_obj.data['email'],email_token)
                    sms_otp_to_user(request,serializer_obj.data['phone'])
                    hash_pass = make_password(request.data['password'])
                    user = User.objects.all().filter(email=request.data['email']).update(password=hash_pass,email_token=email_token)
                   
                    
                    return Response({"Message":"User Register Successfully" ,"user":serializer_obj.data,},status=status.HTTP_200_OK)

                return Response( {"Message":serializer_obj.errors} ,status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response( {"Message":"Bad Request"} ,status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
         print(e)
         Response( {"Message":"Internal Server Error"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserLoginView(APIView):

    try :
        
        serializer_class = LoginSerializer
        @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            )
        )
        def post(self,request,*args,**kwargs):
            
            try:

                serializer = LoginSerializer(data=request.data)
               
                if serializer.is_valid():
                   
                    email = serializer.data['email']
                    password = serializer.data['password']
                    
                    user = authenticate(request,email=email,password=password)
                   
                    if user is not None :
                        
                        if user.is_verified:
                            login(request, user)
                            refresh = RefreshToken.for_user(user)
                            access_token = str(refresh.access_token)
                            refresh_token = str(refresh)

                            return Response( {"Message":"Login Successfully", 'access_token': access_token,
                                            'refresh_token': refresh_token,},status=status.HTTP_200_OK)
                        else:

                            return Response( {"Message: User is not verified"} ,status=status.HTTP_401_UNAUTHORIZED)    
                   
                    else:

                        return Response( {"Message: Invalid Username And Password"} ,status=status.HTTP_401_UNAUTHORIZED)
                        
                        

                return Response( {"Message": serializer.errors } ,status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                 print(e)
                 Response( {"Message:Something Went Wrong"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        print(e)
        Response( {"Message:Something Went Wrong"} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogoutView(APIView):

    @swagger_auto_schema(
    responses={200: 'OK', 401: 'Unauthorized'},
    )
    def get(self, request, format=None):
        
        logout(request)

        return Response( {"Message:Logout Successfull"} ,status=status.HTTP_200_OK)
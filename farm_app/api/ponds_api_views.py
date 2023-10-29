from django.shortcuts import render
from ..serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import DatabaseError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class PondView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all ponds",
        responses={200: PondSerializer(many=True)},
    )
    def get(self, request,*args,**kwargs):
        
        try:
           
            all_pond = Pond.objects.all()

            serializer = PondSerializer(all_pond,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new pond",
        request_body=PondSerializer,
        responses={201: PondSerializer},
    )
    def post(self, request, format=None):
        
        try:
            serializer = PondSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'Pond Created Successfully',
                    'Response': serializer.data
                    }
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PondDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

   
    def get_object(self, pk):

            try:
                return Pond.objects.get(pk=pk)
            except Pond.DoesNotExist:
                return None
    
    
    def get(self, request,pk=None,*args,**kwargs):
        
        try:
           
            if pk is not None:

                pond_instance = self.get_object(pk)
                
                if pond_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = PondSerializer(pond_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Update a pond by ID",
        request_body=PondSerializer,
        responses={200: PondSerializer},
    )
    def put(self, request,pk,*args,**kwargs):

            try:
                pond_instance = self.get_object(pk)
                if pond_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = PondSerializer(pond_instance,data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    Pond.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                    response_data = {
                            'message': 'Pond Updated Successfully ',
                            'Response': serializer.data
                        }
                    return Response(response_data, status=status.HTTP_200_OK)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Delete a pond by ID",
        responses={204: "Resource deleted successfully"},
    )
    def delete(self, request,pk,*args,**kwargs):

        try:
            pond_instance = self.get_object(pk)

            if pond_instance is None:
                        return Response({"detail": "Resource not found."},
                                        status=status.HTTP_404_NOT_FOUND)

            pond_instance.delete()
            return Response({"message": "Resource deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)







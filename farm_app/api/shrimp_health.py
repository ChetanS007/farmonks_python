from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import ShrimpHealthSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.db import DatabaseError



class ShrimpHealthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    @swagger_auto_schema(
        operation_description="Get a list of all shrimphealth",
        responses={200: ShrimpHealthSerializer(many=True)},
    )
    def get(self, request, pk=None):
        
        try:
            

            all_ShrimpHealth = ShrimpHealth.objects.all()

            serializer = ShrimpHealthSerializer(all_ShrimpHealth,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new shrimp health",
        request_body=ShrimpHealthSerializer,
        responses={201: ShrimpHealthSerializer},
    )
    def post(self, request, format=None):
        try:
            serializer = ShrimpHealthSerializer(data=request.data,context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'ShrimpHealth Created Successfully',
                    'Response': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    




class ShrimpHealthDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Get a Biomass record by primary key (pk)
        try:
            return ShrimpHealth.objects.get(pk=pk)
        except ShrimpHealth.DoesNotExist:
            return None

    def get(self, request, pk=None):
        
        try:
            if pk is not None:

                ShrimpHealth_instance = self.get_object(pk)
                
                if ShrimpHealth_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = ShrimpHealthSerializer(ShrimpHealth_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

   
        
    @swagger_auto_schema(
        operation_description="Update a ShrimpHealth by ID",
        request_body=ShrimpHealthSerializer,
        responses={200: ShrimpHealthSerializer},
    )
    def put(self, request, pk):
            try:
               
                wt_instance = self.get_object(pk)
                
                if wt_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = ShrimpHealthSerializer(wt_instance,data=request.data)
                
                if serializer.is_valid():


                    post_serializer = ShrimpHealthSerializer(data=request.data,context={'request': request})

                    if post_serializer.is_valid():
                        post_serializer.save()
                        ShrimpHealth.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                        response_data = {
                            'message': 'ShrimpHealth Created Successfully With Existing ShrimpHealth',
                            'Response': serializer.data
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a ShrimpHealth by ID",
        responses={204: "Resource deleted successfully"},
    )
    def delete(self, request,pk,*args,**kwargs):
        try:
                wt_instance = self.get_object(pk)

                if wt_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                wt_instance.delete()
                return Response({"message": "Resource deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

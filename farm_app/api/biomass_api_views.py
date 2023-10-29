from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Biomass
from ..serializers import BiomassSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from django.db import DatabaseError


class BiomassView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all biomass",
        responses={200: BiomassSerializer(many=True)},
    )
    def get(self, request,):
        
        try:
           
            all_biomass = Biomass.objects.all()

            serializer = BiomassSerializer(all_biomass,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new biomass",
        request_body=BiomassSerializer,
        responses={201: BiomassSerializer},
    )
    def post(self, request, format=None):
        try:
            serializer = BiomassSerializer(data=request.data,context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'Biomass Created Successfully',
                    'Response': serializer.data
                    }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class BiomassDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Get a Biomass record by primary key (pk)
        try:
            return Biomass.objects.get(pk=pk)
        except Biomass.DoesNotExist:
            return None

    def get(self, request, pk=None):
        
        try:
            if pk is not None:

                biomass_instance = self.get_object(pk)
                
                if  biomass_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = BiomassSerializer(biomass_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    
        
    @swagger_auto_schema(
        operation_description="Update a pond by ID",
        request_body=BiomassSerializer,
        responses={200: BiomassSerializer},
    )
    def put(self, request, pk):
        # Update a specific Biomass record
            try:
                
                biomass_instance = self.get_object(pk)
                
                if  biomass_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = BiomassSerializer( biomass_instance,data=request.data)
                
                if serializer.is_valid():


                    post_serializer = BiomassSerializer(data=request.data,context={'request': request})

                    if post_serializer.is_valid():
                        post_serializer.save()
                        Biomass.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                        response_data = {
                            'message': 'Biomass Created Successfully With Existing Biomass',
                            'Response': serializer.data
                        }
                        
                        return Response(response_data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a pond by ID",
        responses={204: "Resource deleted successfully"},
    )
    def delete(self, request,pk,*args,**kwargs):
        try:
                biomass_instance = self.get_object(pk)

                if biomass_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                biomass_instance.delete()
                return Response({"message": "Resource deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)






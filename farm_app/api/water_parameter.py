from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Biomass, WaterParameter
from ..serializers import WaterParameterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.db import DatabaseError



class WaterParameterDetail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Get a feed record by primary key (pk)
        try:
            return WaterParameter.objects.get(pk=pk)
        except WaterParameter.DoesNotExist:
            return None

    def get(self, request, pk=None):
        
        try:
            if pk is not None:

                transaction_instance = self.get_object(pk)
                
                if transaction_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = WaterParameterSerializer(transaction_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

   
    @swagger_auto_schema(
        operation_description="Update a water parameter by ID",
        request_body=WaterParameterSerializer,
        responses={200: WaterParameterSerializer},
    )
    def put(self, request, pk):
            try:
               
                wt_instance = self.get_object(pk)
                
                if wt_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = WaterParameterSerializer(wt_instance,data=request.data)
                
                if serializer.is_valid():


                    post_serializer = WaterParameterSerializer(data=request.data,context={'request': request})

                    if post_serializer.is_valid():
                        post_serializer.save()
                        WaterParameter.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                        response_data = {
                            'message': 'WaterParameter Created Successfully With Existing WaterParameter',
                            'Response': serializer.data
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Delete a water parameter by ID",
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



class WaterParameterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all water parameter",
        responses={200: WaterParameterSerializer(many=True)},
    )
    def get(self, request, pk=None):
        
        try:
            

            all_waterparameter = WaterParameter.objects.all()

            serializer = WaterParameterSerializer(all_waterparameter,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new water parameter",
        request_body=WaterParameterSerializer,
        responses={201: WaterParameterSerializer},
    )
    def post(self, request, format=None):
        try:
            serializer = WaterParameterSerializer(data=request.data,context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'WaterParameter Created Successfully',
                    'Response': serializer.data
                    }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    
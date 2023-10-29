from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import PricingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.db import DatabaseError



class PricingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all pricing health",
        responses={200: PricingSerializer(many=True)},
    )
    def get(self, request, pk=None):
        
        try:
            all_Pricing = Pricing.objects.all()

            serializer = PricingSerializer(all_Pricing,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new pricing health",
        request_body=PricingSerializer,
        responses={201: PricingSerializer},
    )
    def post(self, request, format=None):
        try:
            serializer = PricingSerializer(data=request.data,context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'Pricing Created Successfully',
                    'Response': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    

class PricingDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Get a Biomass record by primary key (pk)
        try:
            return Pricing.objects.get(pk=pk)
        except Pricing.DoesNotExist:
            return None

    def get(self, request, pk=None):
        
        try:
            if pk is not None:

                Pricing_instance = self.get_object(pk)
                
                if Pricing_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = PricingSerializer(Pricing_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a Pricing by ID",
        request_body=PricingSerializer,
        responses={200: PricingSerializer},
    )
    def put(self, request, pk):
            try:
               
                wt_instance = self.get_object(pk)
                
                if wt_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = PricingSerializer(wt_instance,data=request.data)
                
                if serializer.is_valid():


                    post_serializer = PricingSerializer(data=request.data,context={'request': request})

                    if post_serializer.is_valid():
                        post_serializer.save()
                        Pricing.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                        response_data = {
                            'message': 'Pricing Created Successfully With Existing Pricing',
                            'Response': serializer.data
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a Pricing by ID",
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


    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Biomass, Feed
from ..serializers import FeedSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.db import DatabaseError



class FeedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of all feed",
        responses={200: FeedSerializer(many=True)},
    )
    def get(self, request,):
        
        try:
           
            all_Feed = Feed.objects.all()

            serializer = FeedSerializer(all_Feed,many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
   
    @swagger_auto_schema(
        operation_description="Create a new feed",
        request_body=FeedSerializer,
        responses={201: FeedSerializer},
    )
    def post(self, request, format=None):
        try:
            serializer = FeedSerializer(data=request.data,context={'request': request})

            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'message': 'Feed Created Successfully',
                    'Response': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response("An error occurred while creating a Pond.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    


class FeedDetails(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        # Get a Feed record by primary key (pk)
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            return None

    def get(self, request, pk=None):
        
        try:
            if pk is not None:

                feed_instance = self.get_object(pk)
                
                if feed_instance is None:
                    return Response({"detail": "Resource not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                serializer = FeedSerializer(feed_instance)

                return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:

            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update a feed by ID",
        request_body=FeedSerializer,
        responses={200: FeedSerializer},
    )
    def put(self, request, pk):
            try:
               
                wt_instance = self.get_object(pk)
                
                if wt_instance is None:
                            return Response({"detail": "Resource not found."},
                                            status=status.HTTP_404_NOT_FOUND)

                
                serializer = FeedSerializer(wt_instance,data=request.data)
                
                if serializer.is_valid():


                    post_serializer = FeedSerializer(data=request.data,context={'request': request})

                    if post_serializer.is_valid():
                        post_serializer.save()
                        Feed.objects.all().filter(id=pk).update(last_updatedBy=request.user.id)
                        response_data = {
                            'message': 'Feed Created Successfully With Existing Feed',
                            'Response': serializer.data
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 return Response({"Message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a feed by ID",
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

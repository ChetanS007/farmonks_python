from rest_framework import serializers
from .models import *
from .models import Biomass
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


class BaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Get the currently authenticated user
        user = self.context['request'].user
        validated_data['createdBy'] = user  # Set created_by to the authenticated user
        validated_data['last_updatedBy'] = None  # Set last_updated_by to None initially
        print("==",validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Create a new instance to generate a new ID
        return super().update(instance,validated_data)


class PondSerializer(BaseSerializer):
    class Meta:
        model = Pond
        exclude = ('createdBy', 'last_updatedBy') 




class BiomassSerializer(BaseSerializer):
    class Meta:
        model = Biomass
        exclude = ('createdBy', 'last_updatedBy')  # Exclude the 'id' field



class WaterParameterSerializer(BaseSerializer):
    class Meta:
        model = WaterParameter
        exclude = ('createdBy', 'last_updatedBy') 

class FeedSerializer(BaseSerializer):
    class Meta:
        model = Feed
        exclude = ('createdBy', 'last_updatedBy') 

class ShrimpHealthSerializer(BaseSerializer):
    class Meta:
        model = ShrimpHealth
        exclude = ('createdBy', 'last_updatedBy') 

class PricingSerializer(BaseSerializer):
    class Meta:
        model = Pricing
        exclude = ('createdBy', 'last_updatedBy') 

class BasicDetailsSerializer(BaseSerializer):
    class Meta:
        model = BasicDetails
        exclude = ('createdBy', 'last_updatedBy') 

class AddressDetailsSerializer(BaseSerializer):
    class Meta:
        model = AddressDetails
        exclude = ('createdBy', 'last_updatedBy') 


class FarmDetailsSerializer(BaseSerializer):
    class Meta:
        model = FarmDetails
        exclude = ('createdBy', 'last_updatedBy') 

    

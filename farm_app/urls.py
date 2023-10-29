from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from farm_app.api.feed_api import FeedDetails, FeedView
from farm_app.api.shrimp_health import ShrimpHealthDetail, ShrimpHealthView
from farm_app.api.water_parameter import WaterParameterDetail, WaterParameterView
from .views import *
from .api.ponds_api_views import *
from .api.biomass_api_views import *
from .api.pricing_api_views import *
from .api.basic_details import *
from .api.address_details import *
from .api.farm_details import *

urlpatterns = [
    path('verify/<str:token>',VerifyEmail.as_view(),name='verify'),
    path('api/register/',RegisterUser.as_view(),name='register'),

    path('login/',UserLoginView.as_view(),name='login'),
    path('api/v1/logout/', UserLogoutView.as_view(), name='logout'),

    path('api/v1/ponds/', PondView.as_view(), name='pond-list'),
    path('api/v1/ponds/<int:pk>/', PondDetails.as_view(), name='pond-list'),

    path('api/v1/biomass/', BiomassView.as_view(), name='biomass-list'),
    path('api/v1/biomass/<int:pk>/', BiomassDetail.as_view(), name='biomass-list'),

    path('api/v1/waterparameter/', WaterParameterView.as_view(), name='waterparameter-list'),
    path('api/v1/waterparameter/<int:pk>/', WaterParameterDetail.as_view(), name='waterparameter-list'),

    path('api/feed/', FeedView.as_view(), name='feed-list'),
    path('api/feed/<int:pk>/', FeedDetails.as_view(), name='feed-list'),

    path('api/shrimphealth/', ShrimpHealthView.as_view(), name='shrimphealth-list'),
    path('api/shrimphealth/<int:pk>/', ShrimpHealthDetail.as_view(), name='shrimphealth-list'),

    path('api/pricing/', PricingView.as_view(), name='pricing-list'),
    path('api/pricing/<int:pk>/', PricingDetail.as_view(), name='pricing-list'),

    path('api/basicdetails/', BasicDetailsView.as_view(), name='basicdetails-list'),
    path('api/basicdetails/<int:pk>/', BasicDetailsList.as_view(), name='basicdetails-list'),

    path('api/addressdetails/', AddressDetailsView.as_view(), name='addressdetails-list'),
    path('api/addressdetails/<int:pk>/', AddressDetailsList.as_view(), name='addressdetails-list'),

    path('api/farmdetails/', FarmDetailsView.as_view(), name='farmdetails-list'),
    path('api/farmdetails/<int:pk>/',FarmDetailsList.as_view(), name='farmdetails-list'),   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('verify/<str:token>',VerifyEmail.as_view(),name='verify'),
    path('api/register/',RegisterUser.as_view(),name='register'),

    path('api/login/',UserLoginView.as_view(),name='login'),
     path('api/logout/', UserLogoutView.as_view(), name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

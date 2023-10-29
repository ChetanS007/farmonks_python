from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .config import ROLE_TYPE
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin     = True
        user.is_active    = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    first_name  = models.CharField(max_length=250, blank=True, null=True)
    last_name   = models.CharField(max_length=250, blank=True, null=True)
    phone       = models.CharField(max_length=100, unique=True)
    role_type     = models.CharField(max_length=20, choices=ROLE_TYPE)
    is_superadmin = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='photo/',max_length=255,null=True,blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    is_active       = models.BooleanField(default=True, help_text = 'Enable or disable user account')
    deletion_date = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_admin           = models.BooleanField(default=False)

    email_token        = models.CharField(max_length=250, blank=True, null=True)
    is_verified        = models.BooleanField(default=False)
    terms_n_conditions = models.BooleanField(default=False)


   

    objects         = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
	    # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
	    # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return f'{self.email}'



class Pond(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_ponds' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_ponds' , on_delete=models.CASCADE,null=True)
    pond_number = models.CharField(max_length=250,)
    pond_type  = models.CharField(max_length=250,)
    stoking_date = models.DateTimeField()
    total_aerator_capacity = models.CharField(max_length=250,)
    pond_wsa = models.CharField(max_length=250,)
    pond_depth = models.CharField(max_length=250,)
    estimated_harvest_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond_number}'



class Biomass(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_biomass' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_biomass' , on_delete=models.CASCADE,null=True)
    pond = models.ForeignKey(Pond, related_name='pond' , on_delete=models.CASCADE)
    species = models.CharField(max_length=250,)
    pl_stocking_size = models.CharField(max_length=250,)
    days_of_culture = models.CharField(max_length=250,)
    estimated_survival_rate = models.CharField(max_length=250,)
    stocking_density = models.CharField(max_length=250,)
    seed_supplier = models.CharField(max_length=250,)
    avg_body_weight = models.CharField(max_length=250,)
    estimated_biomass = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond}{"-"}{self.species}'


class WaterParameter(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_waterparamter' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_waterparameter' , on_delete=models.CASCADE,null=True)
    pond = models.ForeignKey(Pond, related_name='pond_waterparameter' , on_delete=models.CASCADE)
    tempreature = models.CharField(max_length=250,)
    ph = models.CharField(max_length=250, )
    salinity = models.CharField(max_length=250,)
    total_ammonia_nitogen = models.CharField(max_length=250,)
    nitrite = models.CharField(max_length=250,)
    total_dissolved_solids = models.CharField(max_length=250, )
    dissolved_oxygen = models.CharField(max_length=250,)
    hardness = models.CharField(max_length=250, )
    alkalinity =models.CharField(max_length=250, )
    unionized_ammonia  = models.CharField(max_length=250, )
    nitrate = models.CharField(max_length=250, )
    vibrio_luminance = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond}{"-"}{self.ph}'


class Feed(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_feed' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_feed' , on_delete=models.CASCADE,null=True)
    pond = models.ForeignKey(Pond, related_name='pond_feed' , on_delete=models.CASCADE)
    feed_supplier = models.CharField(max_length=250,)
    feeding_schedule= models.CharField(max_length=250, )
    total_feed_consumed = models.CharField(max_length=250,)
    feed_price = models.CharField(max_length=250,blank=True,null=True)
    feed_used = models.CharField(max_length=250, )
    feed_method = models.CharField(max_length=250,blank=True,null=True)
    feed_conversion_ratio= models.CharField(max_length=250,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond}{"-"}{self.feed_supplier}'


class ShrimpHealth(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_shrimphealth' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_shrimphealth' , on_delete=models.CASCADE,null=True)
    pond = models.ForeignKey(Pond, related_name='pond_shrimphealth' , on_delete=models.CASCADE)
    status = models.CharField(max_length=250,)
    test_conducted = models.CharField(max_length=250, )
    disease_type = models.CharField(max_length=250, )
    lab_name = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond}{"-"}{self.status}'



class Pricing(models.Model):

    createdBy = models.ForeignKey(User, related_name='created_pricing' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_pricing' , on_delete=models.CASCADE,null=True)
    pond = models.ForeignKey(Pond, related_name='pond_pricing' , on_delete=models.CASCADE)
    expected_count = models.CharField(max_length=250, )
    expected_market_rate = models.CharField(max_length=250,)
    current_market_rate = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pond}{"-"}{self.expected_count}'



class BasicDetails(models.Model):
    createdBy = models.ForeignKey(User, related_name='created_basicdetails' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_basicdetails' , on_delete=models.CASCADE,null=True)
    farm_name = models.CharField(max_length=250,)
    farm_ownername = models.CharField(max_length=250,)
    contact_number = models.CharField(max_length=250, blank=True, null=True,unique=True)
    CAA_registration_number = models.CharField(max_length=250,)
    contact_person_name = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.farm_name}'



class AddressDetails(models.Model):
    createdBy = models.ForeignKey(User, related_name='created_addressdetails' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_addressdetails' , on_delete=models.CASCADE,null=True)
    basic_details = models.ForeignKey(BasicDetails, related_name='basicdetails' , on_delete=models.CASCADE)
    address_line = models.CharField(max_length=250,)
    village = models.CharField(max_length=250,)
    district = models.CharField(max_length=250,)
    zip_or_postal_code = models.CharField(max_length=250,)
    taluka = models.CharField(max_length=250,)
    state = models.CharField(max_length=250,)
    country = models.CharField(max_length=250,)
    use_address_for_payment = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address_line}'

class FarmDetails(models.Model):
    createdBy = models.ForeignKey(User, related_name='created_farmdetails' , on_delete=models.CASCADE)
    last_updatedBy = models.ForeignKey(User, related_name='updated_farmdetails' , on_delete=models.CASCADE,null=True)
    basic_details = models.ForeignKey(BasicDetails, related_name='basicdetails_farm' , on_delete=models.CASCADE)
    address_details = models.ForeignKey(AddressDetails, related_name='addressdetails' , on_delete=models.CASCADE)
    water_spread_area = models.CharField(max_length=250,)
    water_source = models.CharField(max_length=250,)
    energy_source = models.CharField(max_length=250,)
    number_of_ponds = models.CharField(max_length=250,)
    nursery_avaliability = models.CharField(max_length=250,)
    land_water_connectivity = models.CharField(max_length=250,)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.water_spread_area}{"-"}{self.address_details}'
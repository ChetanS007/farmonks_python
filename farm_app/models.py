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
    is_admin        = models.BooleanField(default=False)

    email_token   = models.CharField(max_length=250, blank=True, null=True)
    is_verified        = models.BooleanField(default=False)


   

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
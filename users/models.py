from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings


ROLE_CHOICES = (
    ('driver', 'driver'),
    ('merchant','merchant'),
    ('admin','admin')
)


# Manges the creation of custom user
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

# This is custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    last_name = None  # Remove the last_name field

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            ),
            MinLengthValidator(10),
            MaxLengthValidator(10),
        ]
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} {self.last_name}"
    
class AdPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    google_ads_opt_in = models.BooleanField(default=False)
    facebook_ads_opt_in = models.BooleanField(default=False)
    metrad_opt_in = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.name} {self.user.last_name}"


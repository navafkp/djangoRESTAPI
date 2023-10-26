from django.db import models
from phone_field import PhoneField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email_address'), unique=True)
    phone = models.CharField(help_text='Contact phone number', unique=True)
   
    
    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
class UserImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

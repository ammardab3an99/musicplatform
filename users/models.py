from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ExUser(AbstractUser):
    
    bio = models.CharField(max_length=256, default="my simple bio.")
    
    def clean_email(self):
        self.email = self.email.lower()
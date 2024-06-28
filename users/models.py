from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class MyUser(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'



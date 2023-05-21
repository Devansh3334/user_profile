from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=2)
    ''' user_status => {1 : Draft, 2 : Active, 3 : In-Active} '''
    profile_image = models.ImageField(upload_to='Temp')
    designation = models.CharField(max_length=50)
    date_of_birth = models.DateField()




from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    p_image = models.ImageField(upload_to='image', default='')

class Cart(models.Model):
    # foreign keys are created by referring to the object Pet and User
    pid = models.ForeignKey(Pet, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Orders(models.Model):
    orderid = models.IntegerField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.IntegerField()


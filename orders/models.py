from django.db import models

# Create your models here.
from django.db import models

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    # Add more fields as per your requirements
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number
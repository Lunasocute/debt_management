from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.

class Consumer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    ssn = models.CharField(max_length=11)
    
    def __str__(self):
        return self.name
    
class Agency(models.Model):
    name = models.CharField(max_length=100)

class Client(models.Model):
    name = models.CharField(max_length=100)    

class Account(models.Model):
    STATUS_CHOICES = [
        (0, 'INACTIVE'),
        (1, 'PAID_IN_FULL'),
        (2, 'IN_COLLECTION'),
    ]
    client_reference_no = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)   # max balance 99999999.99
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    consumers = models.ManyToManyField(Consumer)
    agency = models.ForeignKey(Agency, on_delete = models.CASCADE, null=True)   # Todo
    client = models.ForeignKey(Client, on_delete = models.CASCADE, null=True)

    # Ensure balance is not negative
    def clean(self):
        if float(self.balance) < 0:
            raise ValidationError({'balance': 'Balance must be greater than or equal to zero.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client_reference_no
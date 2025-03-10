from django.db import models

class Car(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
    ]

    SELLER_CHOICES = [
        ('Dealer', 'Dealer'),
        ('Individual', 'Individual'),
    ]

    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    ]

    OWNER_CHOICES = [
        ('First Owner', 'First Owner'),
        ('Second Owner', 'Second Owner'),
        ('Third Owner', 'Third Owner'),
        ('Fourth & Above Owner', 'Fourth & Above Owner'),
        ('Test Drive Car', 'Test Drive Car'),
    ]

    name = models.CharField(max_length=255)
    year = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    km_driven = models.IntegerField()
    fuel = models.CharField(max_length=10, choices=FUEL_CHOICES)
    seller_type = models.CharField(max_length=10, choices=SELLER_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    owner = models.CharField(max_length=20, choices=OWNER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.year})"

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)  # New field
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact_number']

    def __str__(self):
        return self.email

class BBQBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    guests = models.IntegerField()
    
    MAIN_DISHES = [
        ('beef', 'Beef'),
        ('chicken', 'Chicken'),
        ('pork', 'Pork'),
        ('fish', 'Fish'),
    ]
    main_dishes = models.JSONField()  # Store as {"beef": 10, "chicken": 5, ...}
    
    SIDE_DISHES = [
        ('salad', 'Salad'),
        ('corn', 'Corn'),
        ('potatoes', 'Potatoes'),
        ('beans', 'Beans'),
        ('coleslaw', 'Coleslaw'),
    ]
    side_dishes = models.JSONField()  # Store as {"salad": 15, "corn": 10, ...}
    
    DESSERTS = [
        ('ice_cream', 'Ice Cream'),
        ('fruit', 'Fruit'),
    ]
    desserts = models.JSONField()  # Store as {"ice_cream": 20, "fruit": 10}
    
    drinks = models.IntegerField()  # Total number of drinks (same as guests)

    def __str__(self):
        return f"BBQ Booking for {self.user.email} on {self.date}"
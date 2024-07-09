from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact_number']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            max_id = CustomUser.objects.aggregate(max_id=Max("id"))['max_id']
            self.username = f'user_{max_id + 1 if max_id else 1}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
class BBQBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bbq_bookings')
    status = models.IntegerField(default=0)  # 0: Pending, 1: Confirmed, 2: Cancelled, 3: Completed
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    guests = models.IntegerField()
    
    EVENT_TYPES = [
        ('private', 'Private BBQ'),
        ('company', 'Company BBQ'),
        ('wedding', 'Wedding BBQ'),
        ('school', 'School BBQ'),
        ('themed', 'Themed BBQ'),
        ('breakfast', 'Breakfast Catering'),
        ('holiday', 'Holiday Catering'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='private')
    
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
        return f"{self.get_event_type_display()} for {self.user.email} on {self.date}"
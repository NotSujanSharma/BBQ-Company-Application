from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db import models

# Create your models here.
class Campaign(models.Model):
    RECIPIENT_CHOICES = [
        ('all', 'All Subscribers'),
        ('active', 'Active Clients'),
        ('inactive', 'Inactive Clients'),
    ]

    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    recipient_group = models.CharField(max_length=20, choices=RECIPIENT_CHOICES, default='all')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaigns')

    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    open_rate = models.FloatField(default=0)
    click_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[
        ('chef', 'Chef'),
        ('server', 'Server'),
        ('manager', 'Manager'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
# Generated by Django 5.0.2 on 2024-07-09 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_bbqbooking_event_type_alter_bbqbooking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbqbooking',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]

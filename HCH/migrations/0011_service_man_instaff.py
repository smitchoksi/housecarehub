# Generated by Django 5.0.2 on 2024-02-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0010_manager_instaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_man',
            name='instaff',
            field=models.BooleanField(default=True),
        ),
    ]

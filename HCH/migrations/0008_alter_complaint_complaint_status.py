# Generated by Django 5.0.2 on 2024-02-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0007_alter_booking_data_booking_provide_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complaint_status',
            field=models.CharField(choices=[('1', 'Pending'), ('2', 'solved')], default='Pending', max_length=30),
        ),
    ]

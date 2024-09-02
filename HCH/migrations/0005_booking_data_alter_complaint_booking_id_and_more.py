# Generated by Django 5.0.2 on 2024-02-08 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0004_alter_subcategory_subcatimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contactno', models.BigIntegerField()),
                ('address', models.TextField()),
                ('area', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('booking_date_time', models.DateTimeField()),
                ('booking_provide_date', models.DateField()),
                ('booking_provide_time', models.TimeField()),
                ('booking_status', models.CharField(max_length=30)),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.service')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user')),
            ],
        ),
        migrations.AlterField(
            model_name='complaint',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.booking_data'),
        ),
        migrations.AlterField(
            model_name='feedback_rating',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.booking_data'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.booking_data'),
        ),
        migrations.AlterField(
            model_name='sparepart_payment',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.booking_data'),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]

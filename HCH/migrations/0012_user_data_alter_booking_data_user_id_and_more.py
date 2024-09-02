# Generated by Django 5.0.2 on 2024-02-18 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0011_service_man_instaff'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_email', models.EmailField(max_length=254, unique=True)),
                ('u_password', models.CharField(max_length=256)),
                ('u_fname', models.CharField(max_length=50)),
                ('u_lname', models.CharField(max_length=50)),
                ('u_phoneno', models.BigIntegerField()),
                ('u_address', models.TextField(null=True)),
                ('u_area', models.CharField(max_length=30, null=True)),
                ('u_gender', models.CharField(max_length=10, null=True)),
                ('u_age', models.IntegerField()),
                ('u_profilepic', models.ImageField(null=True, upload_to='user')),
            ],
        ),
        migrations.AlterField(
            model_name='booking_data',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.AlterField(
            model_name='carddetails',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.AlterField(
            model_name='feedback_rating',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.AlterField(
            model_name='sparepart_payment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.user_data'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

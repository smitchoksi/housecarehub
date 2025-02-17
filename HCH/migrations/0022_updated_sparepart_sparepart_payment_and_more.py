# Generated by Django 5.0.2 on 2024-03-06 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0021_task_need_sparepart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Updated_sparepart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sparepart_ids', models.ManyToManyField(to='HCH.sparepart')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.task')),
            ],
        ),
        migrations.CreateModel(
            name='Sparepart_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sparepart_amount', models.IntegerField()),
                ('sparepart_tax', models.FloatField()),
                ('sparepart_total_amount', models.FloatField()),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.booking')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.task')),
                ('upi_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.upi_details')),
                ('updated_spareparts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HCH.updated_sparepart')),
            ],
        ),
        migrations.DeleteModel(
            name='Sparepart_payment_details',
        ),
    ]

# Generated by Django 5.0.2 on 2024-04-25 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0032_remove_task_other'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceman',
            name='sm_knowledge_of_work',
        ),
        migrations.AddField(
            model_name='serviceman',
            name='sm_knowledge_of_subcategory',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='HCH.subcategory'),
            preserve_default=False,
        ),
    ]

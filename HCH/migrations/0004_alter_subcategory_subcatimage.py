# Generated by Django 5.0.2 on 2024-02-07 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCH', '0003_alter_category_catimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='subcatimage',
            field=models.ImageField(upload_to='subcategory'),
        ),
    ]

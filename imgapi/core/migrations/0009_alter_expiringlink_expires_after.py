# Generated by Django 4.1.5 on 2023-09-26 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_expiringlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='expires_after',
            field=models.IntegerField(default=350, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)]),
        ),
    ]

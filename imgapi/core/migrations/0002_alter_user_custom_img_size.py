# Generated by Django 4.1.5 on 2023-09-23 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='custom_img_size',
            field=models.IntegerField(blank=True),
        ),
    ]

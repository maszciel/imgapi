# Generated by Django 4.1.5 on 2023-09-28 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_custom_img_size_user_custom_thumbnail_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

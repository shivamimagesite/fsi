# Generated by Django 2.2.2 on 2019-06-22 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_image_photographer'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='comments',
            field=models.CharField(blank=True, default=None, max_length=99999999, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='likes',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]

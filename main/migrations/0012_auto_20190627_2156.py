# Generated by Django 2.2.2 on 2019-06-27 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190627_2155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='download_url',
            new_name='url',
        ),
    ]

# Generated by Django 2.2.13 on 2021-06-10 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20210609_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerorder',
            old_name='user',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='legalorder',
            name='payment',
        ),
    ]

# Generated by Django 2.2.13 on 2021-05-23 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_legalorderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalorder',
            name='legal_user',
        ),
    ]

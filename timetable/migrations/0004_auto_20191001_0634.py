# Generated by Django 2.2.5 on 2019-10-01 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_auto_20190930_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='weekday',
            field=models.CharField(choices=[('3', 'Wednesday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('4', 'Thursday')], max_length=1, verbose_name='Day of the week'),
        ),
    ]

# Generated by Django 2.2.13 on 2021-06-09 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unp', models.CharField(max_length=255, verbose_name='UNP')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address_legal', models.CharField(max_length=255, verbose_name='Legal address')),
                ('address_order', models.CharField(max_length=255, verbose_name='Delivery address')),
                ('contact_person', models.CharField(max_length=50, verbose_name='The contact person')),
                ('phone', models.CharField(max_length=20, verbose_name='Number')),
                ('note', models.TextField(max_length=2000, verbose_name='Note')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('payment', models.SmallIntegerField(choices=[(0, 'Cash'), (1, 'Card'), (2, 'Online')], verbose_name='Payment format')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100, unique=True, verbose_name='Phone')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('points', models.IntegerField(default=0, verbose_name='Points')),
            ],
        ),
    ]

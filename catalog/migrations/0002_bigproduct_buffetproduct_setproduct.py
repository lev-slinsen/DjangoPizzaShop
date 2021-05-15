# Generated by Django 2.2.13 on 2021-05-15 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bigProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorCode', models.CharField(max_length=10, verbose_name='Артикул')),
                ('name', models.CharField(max_length=10, verbose_name='Название')),
                ('wight', models.FloatField(verbose_name='Вес')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Фуршетный товар',
                'verbose_name_plural': 'Фуршетные товары',
            },
        ),
        migrations.CreateModel(
            name='buffetProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorCode', models.CharField(max_length=10, verbose_name='Артикул')),
                ('name', models.CharField(max_length=10, verbose_name='Название')),
                ('wight', models.FloatField(verbose_name='Вес')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Большой товар',
                'verbose_name_plural': 'Большие товары',
            },
        ),
        migrations.CreateModel(
            name='setProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorCode', models.CharField(max_length=10, verbose_name='Артикул')),
                ('name', models.CharField(max_length=10, verbose_name='Название')),
                ('wight', models.FloatField(verbose_name='Вес')),
                ('description', models.TextField(max_length=2000, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Набор',
                'verbose_name_plural': 'Наборы товаров',
            },
        ),
    ]

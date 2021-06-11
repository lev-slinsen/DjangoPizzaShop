# Generated by Django 2.2.13 on 2021-06-11 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('shop', '0014_auto_20210610_0610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='legalorder',
            name='delivery_time',
        ),
        migrations.CreateModel(
            name='CompanyOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('small', 'Small'), ('large', 'Large'), ('none', 'None')], max_length=100, verbose_name='Size')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Quantity')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.Pizza', verbose_name='Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.LegalOrder', verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_addresses_zip_alter_orders_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addresses',
            name='zip',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='reference',
            field=models.CharField(default='Order-Ref: pdKXDpSG6J2ii19FQv13', editable=False, max_length=50, unique=True),
        ),
    ]

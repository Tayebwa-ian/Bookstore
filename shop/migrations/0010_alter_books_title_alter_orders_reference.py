# Generated by Django 4.1.7 on 2023-04-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_orders_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='reference',
            field=models.CharField(default='Order-Ref: bl5D4yfXGq6yx6OpHRqU', editable=False, max_length=50, unique=True),
        ),
    ]
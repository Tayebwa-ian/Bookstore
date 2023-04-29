# Generated by Django 4.1.7 on 2023-04-23 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_addresses_city_alter_addresses_others_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='shop.addresses'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='reference',
            field=models.CharField(default='Order-Ref: xZJQxR3ASdxGXNgv6wZV', editable=False, max_length=50, unique=True),
        ),
    ]
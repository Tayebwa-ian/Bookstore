# Generated by Django 4.1.7 on 2023-04-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_books_title_alter_orders_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='reference',
            field=models.CharField(default='Order-Ref: USjAd8KtzOQ1N71KG96q', editable=False, max_length=50, unique=True),
        ),
    ]

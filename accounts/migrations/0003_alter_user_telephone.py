# Generated by Django 4.1.7 on 2023-04-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

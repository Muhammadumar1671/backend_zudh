# Generated by Django 5.1 on 2024-08-26 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suit', '0002_alter_collar_type_collar_type_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='suit_details',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]

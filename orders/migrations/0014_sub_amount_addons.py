# Generated by Django 2.0.3 on 2018-04-22 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_syc_pizza_amount_toppings'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub',
            name='amount_addons',
            field=models.IntegerField(default=0),
        ),
    ]

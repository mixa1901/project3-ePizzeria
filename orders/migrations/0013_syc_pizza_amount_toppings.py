# Generated by Django 2.0.3 on 2018-04-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_reg_pizza_amount_toppings'),
    ]

    operations = [
        migrations.AddField(
            model_name='syc_pizza',
            name='amount_toppings',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 2.0.3 on 2018-05-05 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0024_auto_20180503_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='topping',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

# Generated by Django 2.0.3 on 2018-05-03 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_auto_20180502_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='addon',
        ),
        migrations.RemoveField(
            model_name='order',
            name='consumer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='size',
        ),
        migrations.RemoveField(
            model_name='order',
            name='topping',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]

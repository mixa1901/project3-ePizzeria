# Generated by Django 2.0.3 on 2018-05-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_remove_topping_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('d', 'Declined'), ('c', 'Completed'), ('p', 'Pending')], default='p', max_length=1),
        ),
    ]
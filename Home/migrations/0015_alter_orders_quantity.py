# Generated by Django 3.2.7 on 2021-10-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0014_alter_orders_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

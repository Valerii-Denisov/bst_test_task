# Generated by Django 4.2.5 on 2023-09-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('api_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersqueue',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order'),
        ),
    ]
# Generated by Django 3.0.3 on 2020-02-15 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_auto_20200215_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='currency',
        ),
    ]

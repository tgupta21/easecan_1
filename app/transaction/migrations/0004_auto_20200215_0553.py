# Generated by Django 3.0.3 on 2020-02-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20200215_0540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='completion_time',
        ),
        migrations.AddField(
            model_name='payment',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

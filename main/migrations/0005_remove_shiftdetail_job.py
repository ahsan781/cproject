# Generated by Django 2.2.24 on 2021-08-16 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210816_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiftdetail',
            name='job',
        ),
    ]

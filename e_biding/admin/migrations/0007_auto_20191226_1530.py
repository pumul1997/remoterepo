# Generated by Django 2.0.5 on 2019-12-26 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_auto_20191224_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='o_status',
            field=models.CharField(max_length=20),
        ),
    ]

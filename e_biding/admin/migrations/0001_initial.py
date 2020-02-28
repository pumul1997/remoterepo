# Generated by Django 2.0.5 on 2019-12-13 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('image', models.ImageField(upload_to='admin_profile/')),
                ('password', models.CharField(max_length=8)),
            ],
        ),
    ]

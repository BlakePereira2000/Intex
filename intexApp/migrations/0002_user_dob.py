# Generated by Django 4.1.2 on 2022-11-30 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intexapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(auto_now=True),
        ),
    ]
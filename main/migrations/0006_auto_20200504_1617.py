# Generated by Django 3.0.5 on 2020-05-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.CharField(default='{}', max_length=100000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.CharField(default='{}', max_length=100000),
        ),
    ]

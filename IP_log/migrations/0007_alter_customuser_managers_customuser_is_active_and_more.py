# Generated by Django 5.0.6 on 2024-07-19 12:19

import IP_log.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IP_log', '0006_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', IP_log.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
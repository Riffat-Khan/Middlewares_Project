# Generated by Django 5.0.6 on 2024-07-15 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IP_log', '0002_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.CharField(choices=[('Gold', 'gold'), ('Silver', 'silver'), ('Bronze', 'bronze'), ('Unauthenticated', 'unauthenticated')], max_length=50),
        ),
    ]

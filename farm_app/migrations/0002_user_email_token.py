# Generated by Django 4.2.3 on 2023-09-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_token',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]

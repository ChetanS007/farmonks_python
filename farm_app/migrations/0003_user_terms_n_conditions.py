# Generated by Django 4.2.3 on 2023-10-21 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_app', '0002_user_email_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='terms_n_conditions',
            field=models.BooleanField(default=False),
        ),
    ]

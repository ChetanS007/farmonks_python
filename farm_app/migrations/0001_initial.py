# Generated by Django 4.2.3 on 2023-09-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(max_length=100, unique=True)),
                ('role_type', models.CharField(choices=[('Farmer', 'Farmer'), ('Organisation', 'Organisation')], max_length=20)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('profile_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='photo/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, help_text='Enable or disable user account')),
                ('deletion_date', models.DateTimeField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

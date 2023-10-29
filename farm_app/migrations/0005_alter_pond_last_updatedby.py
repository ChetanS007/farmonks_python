# Generated by Django 4.2.3 on 2023-10-22 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farm_app', '0004_pond_waterparameter_shrimphealth_pricing_feed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pond',
            name='last_updatedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_ponds', to=settings.AUTH_USER_MODEL),
        ),
    ]

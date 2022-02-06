# Generated by Django 4.0.1 on 2022-02-05 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachingassistant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ta',
            name='user_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
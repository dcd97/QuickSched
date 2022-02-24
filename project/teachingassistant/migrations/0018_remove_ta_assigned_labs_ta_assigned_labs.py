# Generated by Django 4.0.1 on 2022-02-24 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laborganizer', '0006_remove_lab_assigned_ta'),
        ('teachingassistant', '0017_ta_assigned_labs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ta',
            name='assigned_labs',
        ),
        migrations.AddField(
            model_name='ta',
            name='assigned_labs',
            field=models.ManyToManyField(blank=True, to='laborganizer.Lab'),
        ),
    ]

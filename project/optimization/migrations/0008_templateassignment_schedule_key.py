# Generated by Django 4.0.1 on 2022-03-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optimization', '0007_remove_templateassignment_lab_templateassignment_lab_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateassignment',
            name='schedule_key',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Schedule Key'),
        ),
    ]
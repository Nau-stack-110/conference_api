# Generated by Django 3.2.19 on 2025-01-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='price',
            field=models.CharField(default='Gratuit', max_length=255),
        ),
    ]

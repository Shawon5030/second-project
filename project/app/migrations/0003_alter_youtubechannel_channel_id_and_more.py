# Generated by Django 5.1.1 on 2024-12-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_youtubechannel_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubechannel',
            name='channel_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='youtubechannel',
            name='channel_url',
            field=models.CharField(max_length=255),
        ),
    ]
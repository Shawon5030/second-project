# Generated by Django 5.1.1 on 2024-12-26 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_addmoney'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addmoney',
            name='earning',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='addmoney',
            name='payment',
            field=models.IntegerField(),
        ),
    ]
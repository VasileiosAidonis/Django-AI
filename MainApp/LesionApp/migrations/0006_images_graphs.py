# Generated by Django 3.1.1 on 2020-09-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LesionApp', '0005_auto_20200911_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='graphs',
            field=models.TextField(null=True),
        ),
    ]

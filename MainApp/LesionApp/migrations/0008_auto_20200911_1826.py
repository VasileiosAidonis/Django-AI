# Generated by Django 3.1.1 on 2020-09-11 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LesionApp', '0007_auto_20200911_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='pred_list',
            field=models.TextField(blank=True),
        ),
    ]

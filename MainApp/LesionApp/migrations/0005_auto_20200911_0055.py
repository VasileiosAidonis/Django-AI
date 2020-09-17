# Generated by Django 3.1.1 on 2020-09-10 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LesionApp', '0004_images_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='result',
            new_name='result_binary',
        ),
        migrations.AddField(
            model_name='images',
            name='result_multiclass',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-09 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LesionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('gender', models.CharField(max_length=20)),
                ('anatomic_site', models.CharField(max_length=50)),
                ('group_age', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]

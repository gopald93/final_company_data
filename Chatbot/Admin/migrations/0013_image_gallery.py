# Generated by Django 3.1 on 2020-08-31 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0012_auto_20200831_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_Gallery',
            fields=[
                ('image_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('image_path', models.ImageField(unique=True, upload_to='images/')),
            ],
        ),
    ]

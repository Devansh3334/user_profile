# Generated by Django 4.2.1 on 2023-05-20 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]

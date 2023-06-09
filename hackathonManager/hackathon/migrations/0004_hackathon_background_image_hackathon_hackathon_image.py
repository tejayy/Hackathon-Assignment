# Generated by Django 4.2 on 2023-04-19 08:06

from django.db import migrations, models
import hackathon.models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0003_remove_hackathon_background_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to=hackathon.models.upload_to),
        ),
        migrations.AddField(
            model_name='hackathon',
            name='hackathon_image',
            field=models.ImageField(blank=True, null=True, upload_to=hackathon.models.upload_to),
        ),
    ]

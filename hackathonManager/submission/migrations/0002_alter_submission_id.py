# Generated by Django 4.2 on 2023-04-19 07:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3b42f297-fbbc-4bd5-b6ec-e4d752770c12'), primary_key=True, serialize=False),
        ),
    ]

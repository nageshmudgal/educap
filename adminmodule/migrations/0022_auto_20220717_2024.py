# Generated by Django 2.2.28 on 2022-07-17 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0021_batch_videos_name_batch_videos_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='date',
            field=models.DateField(),
        ),
    ]

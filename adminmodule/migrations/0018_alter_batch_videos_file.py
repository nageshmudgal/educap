# Generated by Django 4.0 on 2022-07-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0017_batch_batch_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch_videos',
            name='file',
            field=models.FileField(default='', upload_to='batch_videos/'),
        ),
    ]

# Generated by Django 4.0 on 2022-07-09 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0020_batch_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch_videos',
            name='name',
            field=models.CharField(default='abc', max_length=50),
        ),
        migrations.AddField(
            model_name='batch_videos',
            name='status',
            field=models.CharField(default='active', max_length=10),
        ),
    ]

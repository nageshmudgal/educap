# Generated by Django 4.0 on 2022-07-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0018_alter_batch_videos_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='a',
            field=models.CharField(default='Pm', max_length=50),
        ),
    ]

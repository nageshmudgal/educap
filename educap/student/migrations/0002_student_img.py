# Generated by Django 2.1.5 on 2022-06-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='img',
            field=models.ImageField(default='userimage/userprofile.jpg', upload_to='userimage/'),
        ),
    ]
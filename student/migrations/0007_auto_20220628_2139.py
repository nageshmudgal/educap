# Generated by Django 2.0.7 on 2022-06-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0016_auto_20220628_2139'),
        ('student', '0006_student_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ManyToManyField(to='adminmodule.Course'),
        ),
    ]
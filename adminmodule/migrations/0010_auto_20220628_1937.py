# Generated by Django 2.0.7 on 2022-06-28 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0009_usercourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]

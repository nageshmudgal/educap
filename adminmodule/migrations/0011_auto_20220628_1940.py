# Generated by Django 2.0.7 on 2022-06-28 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminmodule', '0010_auto_20220628_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]

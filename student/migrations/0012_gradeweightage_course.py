# Generated by Django 2.1.2 on 2018-11-11 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_academic_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeweightage',
            name='course',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

# Generated by Django 2.1.2 on 2018-11-11 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_remove_academic_score_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradeschema',
            name='Facultycourse_Id',
        ),
        migrations.RemoveField(
            model_name='gradeweightage',
            name='Facultycourse_Id',
        ),
        migrations.DeleteModel(
            name='Gradeschema',
        ),
        migrations.DeleteModel(
            name='Gradeweightage',
        ),
    ]

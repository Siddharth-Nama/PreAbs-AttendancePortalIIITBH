# Generated by Django 4.2.14 on 2024-08-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_student_user_student_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='123', max_length=1000),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 4.2.14 on 2024-08-02 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='NULL', max_length=100),
        ),
    ]

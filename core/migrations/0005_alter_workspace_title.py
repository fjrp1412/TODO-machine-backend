# Generated by Django 4.0.6 on 2022-08-29 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_todo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='title',
            field=models.CharField(default='Workspace', max_length=255),
        ),
    ]
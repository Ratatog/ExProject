# Generated by Django 5.1.5 on 2025-01-31 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_project_members_alter_project_creator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.TextField(verbose_name='Приоритет'),
        ),
    ]

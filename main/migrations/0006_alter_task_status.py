# Generated by Django 5.1.5 on 2025-01-31 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.TextField(choices=[('active', 'Активна'), ('completed', 'Завершена'), ('paused', 'Приостановлена')], default='active', verbose_name='Статус'),
        ),
    ]

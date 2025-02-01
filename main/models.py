from django.db import models


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активен'
        COMPLETED = 'completed', 'Завершен'
        PAUSED = 'paused', 'Приостановлен'
        
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=200, verbose_name='Описание')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    end_date = models.DateTimeField(default=None, null=True, verbose_name='Дата окончания')
    status = models.TextField(choices=Status.choices, default=Status.ACTIVE, verbose_name='Статус')
    
    creator = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Создатель', related_name='project')
    moders = models.ManyToManyField('users.User', verbose_name='Важные Шишки', related_name='mods')
    members = models.ManyToManyField('users.User', verbose_name='Участники', related_name='mems')
    requests = models.ManyToManyField('users.User', verbose_name='Запросы', related_name='reqs')
    
    class Meta:
        ordering = ['-pk']

class Task(models.Model):
    class Status(models.TextChoices):
        PROGRESS = 'progress', 'Активна'
        COMPLETED = 'completed', 'Завершена'
        NOTSTARTED = 'not_started', 'Не_начата'
    
    class Priority(models.TextChoices):
        HIGH = 'high', 'Высокий'
        MEDIUM = 'medium', 'Средний'
        LOW = 'low', 'Низкий'
        
        
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=200, verbose_name='Описание')
    project = models.ForeignKey('main.Project', on_delete=models.CASCADE, verbose_name='Проект', related_name='tasks')
    priority = models.TextField(choices=Priority.choices, verbose_name='Приоритет')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    end_date = models.DateTimeField(default=None, null=True, verbose_name='Дата окончания')
    status = models.TextField(choices=Status.choices, default=Status.NOTSTARTED, verbose_name='Статус')
    
    taked = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Кем Взято', related_name='tasks')
    
    class Meta:
        ordering = ['priority', '-pk']
    
    @classmethod
    def get_ordered_queyset(cls):
        return cls.objects.annotate(
            order_priority=models.Case(
                models.When(status=cls.Status.COMPLETED, then=4),
                models.When(priority=cls.Priority.HIGH, then=1),
                models.When(priority=cls.Priority.MEDIUM, then=2),
                models.When(priority=cls.Priority.LOW, then=3),
                output_field=models.IntegerField(),
            )
        ).order_by('order_priority')

class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Пользователь', related_name='comms')
    text = models.CharField(max_length=100, verbose_name='Текст')
    task = models.ForeignKey('main.Task', on_delete=models.CASCADE, verbose_name='Задача', related_name='comms')
    
    class Meta:
        ordering = ['-pk']
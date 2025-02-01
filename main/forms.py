from django import forms
from django.contrib.auth import get_user_model
from .models import Project, Task, Comment


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']
        
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
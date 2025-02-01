from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from itertools import chain
from django.utils.timezone import now as tnow
from .forms import CreateProjectForm, CreateTaskForm, CreateCommentForm
from .models import Project, Task, Comment
from .utils import LoginMixn

def to_super(u):
    return not u.is_superuser
def to_creator(u, p):
    return not p.creator == u and to_super(u)
def to_moder(u, p):
    return not u in p.moders.all() and to_creator(u, p)
def to_member(u, p):
    return not u in p.members.all() and to_moder(u, p)

class Home(LoginMixn, TemplateView):
    template_name = 'main/home.html'
    extra_context = {'title': 'Home', 'projects': Project.objects}
    
class CreateProject(LoginMixn, CreateView):
    template_name = 'main/create_project.html'
    form_class = CreateProjectForm
    extra_context = {'title': 'Create Project'}
    
    def get_success_url(self):
        return reverse_lazy('project', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CreateTask(LoginMixn, CreateView):
    template_name = 'main/create_task.html'
    form_class = CreateTaskForm
    extra_context = {'title': 'Create Task'}
    
    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk = self.kwargs['pk'])
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk = self.kwargs['pk'])
        if to_moder(self.request.user, p):
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return super().get(request, *args, **kwargs)
    
class ProjectView(LoginMixn, TemplateView):
    template_name = 'main/project.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        context['tasks'] = Task.get_ordered_queyset().filter(project=context['project'])
        context['title'] = context['project'].title
        return context

class TaskView(LoginMixn, CreateView):
    template_name = 'main/task.html'
    pk_url_kwarg = 'pk'
    form_class = CreateCommentForm
    
    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.kwargs[self.pk_url_kwarg]})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.task = Task.objects.get(pk = self.kwargs[self.pk_url_kwarg])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.t
        context['comms'] = Comment.objects.filter(task=self.t)
        context['title'] = context['task'].title
        return context
    
    def get(self, request, *args, **kwargs):
        self.t = Task.objects.get(pk = self.kwargs[self.pk_url_kwarg])
        if to_member(self.request.user, self.t.project):
            return HttpResponseRedirect(reverse_lazy('home'))

        return super().get(request, *args, **kwargs)
    
class DeleteProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if to_creator(self.request.user, p): 
            return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))
        p.delete()
        return HttpResponseRedirect(reverse_lazy('home'))

class DeleteTask(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        t = Task.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if to_moder(self.request.user, t.project):
            return HttpResponseRedirect(reverse_lazy('task', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))
        t.delete()
        return HttpResponseRedirect(reverse_lazy('task', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class ChangeProject(LoginMixn, UpdateView):
    model = Project
    form_class = CreateProjectForm
    template_name = 'main/change_project.html'
    extra_context = {'title': 'Change Project'}
    
    def get_success_url(self):
        return reverse_lazy('project', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        t = Task.objects.get(pk=kwargs[self.pk_url_kwarg])
        if to_moder(self.request.user, t.project):
            return HttpResponseRedirect('home')
        return super().get(request, *args, **kwargs)
    
class ChangeTask(LoginMixn, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'main/change_task.html'
    extra_context = {'title': 'Change Task'}
    pk_url_kwarg = 'pk'
    
    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        t = Task.objects.get(pk=kwargs[self.pk_url_kwarg])
        if to_moder(self.request.user, t.project):
            return HttpResponseRedirect('home')
        return super().get(request, *args, **kwargs)
    
class JoinProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        p.requests.add(self.request.user)
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class AcceptProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        u = get_user_model().objects.get(pk=self.kwargs['upk'])
        if to_creator(self.request.user, p):
            return HttpResponseRedirect(reverse_lazy('home'))
        p.requests.remove(u)
        p.members.add(u)
        return HttpResponseRedirect(reverse_lazy('project_requests', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))
    
class DeclineProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        u = get_user_model().objects.get(pk=self.kwargs['upk'])
        if to_creator(self.request.user, p):
            return HttpResponseRedirect(reverse_lazy('home'))
        p.requests.remove(u)
        return HttpResponseRedirect(reverse_lazy('project_requests', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class QuitProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        u = get_user_model().objects.get(pk=self.kwargs['upk'])
        p.members.remove(u)
        p.moders.remove(u)
        Task.objects.filter(taked=u).update(taked=None, status=Task.Status.NOTSTARTED)
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))
    
class CancelProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        p.requests.remove(self.request.user)
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class ModerationProject(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        u = get_user_model().objects.get(pk=self.kwargs['upk'])
        if to_creator(self.request.user, p):
            return HttpResponseRedirect(reverse_lazy('home'))
        if u in p.moders.all():
            p.members.add(u)
            p.moders.remove(u)
        else:
            p.members.remove(u)
            p.moders.add(u)
            
        return HttpResponseRedirect(reverse_lazy('project_members', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class TakeTask(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        t = Task.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if t.status == Task.Status.NOTSTARTED:
            t.status = Task.Status.PROGRESS
            t.taked = self.request.user
        else:
            t.status = Task.Status.NOTSTARTED
            t.taked = None
        t.save()
        return HttpResponseRedirect(reverse_lazy('task', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class CompleteTask(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        t = Task.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        t.status = Task.Status.COMPLETED
        t.end_date = tnow()
        t.save()
        return HttpResponseRedirect(reverse_lazy('task', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))

class MembersView(LoginMixn, ListView):
    template_name = 'main/project_members.html'
    context_object_name = 'reqs'
    extra_context = {'title': 'Members'}
    pk_url_kwarg = 'pk'
    
    def get_queryset(self):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        return list(chain(p.members.all(), p.moders.all()))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pid'] = self.kwargs[self.pk_url_kwarg]
        context['proj'] = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        return context
    
class RequestsView(MembersView):
    template_name = 'main/project_requests.html'
    extra_context = {'title': 'Requests'}

    def get_queryset(self):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        return p.requests.all()

class ProjectFinish(LoginMixn, View):
    pk_url_kwarg = 'pk'
    def get(self, request, *args, **kwargs):
        p = Project.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        if to_creator(self.request.user, p):
            return HttpResponseRedirect(reverse_lazy('home'))
        p.end_date = tnow()
        p.status = Project.Status.COMPLETED
        p.save()
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': self.kwargs[self.pk_url_kwarg]}))
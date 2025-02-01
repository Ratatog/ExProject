from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    
    path('create/project/', views.CreateProject.as_view(), name='create_project'),
    path('create/task/<int:pk>/', views.CreateTask.as_view(), name='create_task'),
    
    path('delete/project/<int:pk>/', views.DeleteProject.as_view(), name='delete_project'),
    path('delete/task/<int:pk>/', views.DeleteTask.as_view(), name='delete_task'),
    
    path('change/project/<int:pk>/', views.ChangeProject.as_view(), name='change_project'),
    path('change/task/<int:pk>/', views.ChangeTask.as_view(), name='change_task'),
    
    path('project/<int:pk>/', views.ProjectView.as_view(), name='project'),
    path('task/<int:pk>/', views.TaskView.as_view(), name='task'),
    
    path('join_project/<int:pk>/', views.JoinProject.as_view(), name='join_project'),
    path('cancel_project/<int:pk>/', views.CancelProject.as_view(), name='cancel_project'),
    path('accept_project/<int:pk>/<int:upk>/', views.AcceptProject.as_view(), name='accept_project'),
    path('decline_project/<int:pk>/<int:upk>/', views.DeclineProject.as_view(), name='decline_project'),
    path('quit_project/<int:pk>/<int:upk>/', views.QuitProject.as_view(), name='quit_project'),
    path('mod_project/<int:pk>/<int:upk>/', views.ModerationProject.as_view(), name='mod_project'),
    path('take_task/<int:pk>/', views.TakeTask.as_view(), name='take_task'),
    path('complete_task/<int:pk>/', views.CompleteTask.as_view(), name='complete_task'),
    
    path('project_requests/<int:pk>/', views.RequestsView.as_view(), name='project_requests'),
    path('project_members/<int:pk>/', views.MembersView.as_view(), name='project_members'),
    
    path('project_finish/<int:pk>/', views.ProjectFinish.as_view(), name='project_finish'),
]

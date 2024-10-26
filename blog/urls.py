from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ProjectTasksView, TaskDetailView
from . import views

urlpatterns = [
    path('',PostListView.as_view(), name='blog-home'), #localhost:8000/blog/ 
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'), 
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'), 
    path('post/<int:project_id>/create_task/', views.create_task, name='create-task'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('post/<int:pk>/add_participants/', views.add_participants, name='add_participants'),
    path('task/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),
    path('post/<int:pk>/tasks/', ProjectTasksView.as_view(), name='task-management'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update-task-status'),




]

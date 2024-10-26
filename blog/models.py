from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    chef = models.ForeignKey(User, related_name='projects_managed', on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    description= models.TextField()
    date_posted= models.DateTimeField(default=timezone.now)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='projects_joined')

    
    def __str__(self): #equivalent du toString en java 
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) #return the full path as a string
    def get_tasks_per_participant(self):
         result = {}
         for participant in self.participants.all():
           result[participant] = Task.objects.filter(project=self, assigned_to=participant)
         return result


    
class Task(models.Model):
    STATUS_CHOICES = (
        ('TODO', 'TODO'),
        ('In progress', 'In progress'),
        ('Done', 'Done'),
        ('In revision', 'In revision'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='TODO')
    project= models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Titre par défaut")
    description =models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", default=9)

    def is_user_project_chef(self, user):
      return self.project.chef == user



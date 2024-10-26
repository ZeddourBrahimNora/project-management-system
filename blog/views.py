import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseForbidden

from users.forms import TaskForm
from .models import Post
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import DetailView
from .models import Task
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, User
from django.contrib import messages
from django.http import JsonResponse

from django.views.generic.detail import DetailView
from .models import Post


# Create your views here. 


def home(request):
    #creation d'un objet context -> dictionnaire qui contient une seule entrée qui a pour valeur la liste des posts
    context = {
        'posts' : Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)


def create_task(request, project_id):
    project = Post.objects.get(pk=project_id)
     # Restreindre l'accès seulement au chef du projet
    if request.user != project.chef:
        return HttpResponse("Vous n'avez pas le droit de créer une tâche pour ce projet.", status=403)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('post-detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'blog/create_task.html', {'form': form})




def add_participants(request, pk):
    project = get_object_or_404(Post, id=pk)
    
    # Vérifier si l'utilisateur courant est le chef du projet
    if request.user == project.chef:
        
        if request.method == 'POST':
            # Récupérer l'utilisateur à partir du formulaire (à adapter selon votre formulaire)
            user_id = request.POST.get('user_id')
            user_to_add = get_object_or_404(User, id=user_id)
            
            # Ajouter cet utilisateur aux participants
            project.participants.add(user_to_add)
            messages.success(request, f"{user_to_add.username} a été ajouté au projet!")
            
            return redirect('post-detail', pk=pk)
        
        # Si la requête est un GET, affichez le formulaire pour sélectionner un utilisateur
        else:
            # Exclure les utilisateurs déjà participants
            users = User.objects.exclude(id__in=project.participants.all())
            return render(request, 'blog/add_participants.html', {'users': users})
    
    else:
        messages.warning(request, "Vous n'êtes pas autorisé à ajouter des participants à ce projet.")
        return redirect('post-detail', pk=pk)

#pour mettre a jour le status avec Ajax
from django.http import JsonResponse
from .models import Task

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json

@csrf_exempt
def update_task_status(request, task_id):
    if request.method == 'POST' and request.content_type == 'application/json':
        data = json.loads(request.body.decode('utf-8'))
        new_status = data.get('status')
        
        if not new_status:
            return JsonResponse({"success": False, "message": "Statut manquant dans la requête."})

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "message": "Tâche non trouvée."})
        
        task.status = new_status
        task.save()

        return JsonResponse({"success": True, "message": "Statut mis à jour avec succès."})
    
    return JsonResponse({"success": False, "message": "Requête non valide."})


def get_assigned_tasks(self, project):
    return Task.objects.filter(project=project, assigned_to=self)


#drag and drop tasks
class ProjectTasksView(DetailView):
    model = Post
    template_name = 'blog/task_management.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks_todo"] = self.object.task_set.filter(status="TODO")
        context["tasks_in_progress"] = self.object.task_set.filter(status="In Progress")
        context["tasks_done"] = self.object.task_set.filter(status="Done")
        context["tasks_in_revision"] = self.object.task_set.filter(status="In Revision")
        context["tasks_per_participant"] = self.object.get_tasks_per_participant()
        return context


class PostListView(ListView):
    model = Post 
    template_name = 'blog/home.html' #<app>/<model>_>viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] 
 

class PostDetailView(DetailView):
    model = Post 

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title','description']
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        form.instance.chef = self.request.user  # Définir le chef du projet
        return super().form_valid(form)
    


class TaskDetailView(DetailView):
    model = Task
    template_name = 'blog/task_detail.html'  # <--- Assume your app name is 'blog'
    context_object_name = 'task'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post 
    fields = ['title','description']
    
    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: 
            return True
        return False

class PostDeleteView( LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     model = Post 
     success_url = '/'
    
     def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: 
            return True
        return False

 
#def about(request):
 #   return render(request, 'blog/about.html', {'title': 'my about page'})





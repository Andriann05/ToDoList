from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # L'utilisateur devra se connecter manuellement
    else:
        form = SignUpForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirection après connexion
    else:
        form = AuthenticationForm()
    return render(request, "tasks/login.html", {"form": form})

def logout_view(request):
    logout(request)  # Supprime la session de l'utilisateur
    request.session.flush()  # Vide toutes les données de session
    return redirect('login')  # Redirige vers la connexion

def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    urgent_important = tasks.filter(priority='urgent_important')
    not_urgent_important = tasks.filter(priority='important_not_urgent')
    urgent_not_important = tasks.filter(priority='urgent_not_important')
    not_urgent_not_important = tasks.filter(priority='not_urgent_not_important')

    context = {
        'urgent_tasks': urgent_important.exists(),  
        'urgent_important': urgent_important,
        'not_urgent_important': not_urgent_important,
        'urgent_not_important': urgent_not_important,
        'not_urgent_not_important': not_urgent_not_important,
    }

    return render(request, 'tasks/task_list.html', context)

@login_required
def home(request):
    return render(request, "tasks/home.html")

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associe la tâche à l'utilisateur connecté
            task.save()

            # Vérifie si la tâche est urgente (ajoute un champ "urgent" dans le modèle)
            if task.urgent:
                # Assurez-vous que le champ urgent existe dans le modèle Task
                subject = f"🔔 Rappel : '{task.title}' arrive bientôt !"
                message = f"Bonjour {task.user.username},\n\n"
                message += f"La tâche '{task.title}' doit être terminée avant le {task.due_date}.\n"  # Correction ici
                message += "Pensez à la terminer à temps ! 🚀\n\n"
                message += "Cordialement,\nVotre gestionnaire de tâches."
                
                send_mail(
                    subject,
                    message,
                    'ramiandrisoan5@gmail.com',  # Expéditeur
                    [task.user.email],  # Destinataire dynamique
                    fail_silently=False,
                )

            return redirect('task_list')  # Redirige vers la liste des tâches
    else:
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/delete_task.html', {'task': task})

@login_required
def mark_as_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if not task.completed:  # Vérifie si la tâche n'est pas déjà terminée
        task.completed = True
        task.save()
    
    return redirect('task_list')


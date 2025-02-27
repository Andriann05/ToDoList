from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Task  # Modifie selon ton modèle de tâche

def send_task_reminders():
    """Envoie des rappels pour les tâches urgentes."""
    urgent_tasks = Task.objects.filter(deadline__lte=now(), completed=False)

    for task in urgent_tasks:
        user_email = task.user.email  # Adapte selon ton modèle
        subject = f"🔔 Rappel : Tâche urgente '{task.title}'"
        message = f"Bonjour {task.user.username},\n\n"
        message += f"Votre tâche '{task.title}' a une échéance aujourd'hui ({task.deadline}). Pensez à la terminer !\n\n"
        message += "Bonne journée,\nTon application Task List 📋"

        send_mail(subject, message, 'ramiandrisoan5@gmail.com', [user_email])

    print(f"{urgent_tasks.count()} rappels envoyés.")

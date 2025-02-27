import time
from django.core.mail import send_mail
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = "Envoie des rappels pour les tâches proches de la deadline"

    def handle(self, *args, **kwargs):
        today = now().date()
        tasks = Task.objects.filter(due_date__gt=today, completed=False)  # Correction ici

        for task in tasks:
            if not task.user or not task.user.email:  # Vérifier si l'utilisateur a un email
                continue  

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

        self.stdout.write(self.style.SUCCESS('📩 Rappels envoyés avec succès !'))
        time.sleep(3600)
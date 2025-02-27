from django.core.mail import send_mail
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = "Envoie des rappels pour les tâches proches de la deadline"

    def handle(self, *args, **kwargs):
        today = now().date()
        tasks = Task.objects.filter(deadline__gt=today, completed=False)  # Tâches à venir

        for task in tasks:
            send_mail(
                'Rappel : tâche à faire bientôt !',
                f"La tâche '{task.title}' doit être terminée avant le {task.deadline}.",
                'ramiandrisoan5@gmail.com',  # Expéditeur
                ['nyainaandrianina248@gmail.com'],  # Remplace par l'email du destinataire
                fail_silently=False,
            )
        
        self.stdout.write(self.style.SUCCESS('Rappels envoyés avec succès !'))

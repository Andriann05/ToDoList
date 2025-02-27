from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.timezone import now
from tasks.models import Task

@receiver(post_save, sender=Task)
def send_task_reminder(sender, instance, created, **kwargs):
    """Envoie un email si une tâche urgente est ajoutée"""
    if created and instance.due_date.date() <= now().date():
        if instance.user and instance.user.email:  # Vérifier si l'utilisateur a un email
            send_mail(
                "⚠️ Nouvelle tâche urgente ajoutée !",
                f"Bonjour {instance.user.username},\n\n"
                f"Vous avez ajouté une tâche urgente : '{instance.title}', à terminer avant le {instance.due_date}.\n"
                "Merci de la compléter rapidement ! 🕒\n\n"
                "Cordialement,\nVotre gestionnaire de tâches.",
                "ramiandrisoan5@gmail.com",  # Expéditeur
                [instance.user.email],  # Destinataire
                fail_silently=False,
            )

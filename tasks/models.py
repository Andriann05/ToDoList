from django.db import models
from django.conf import settings  # Pour récupérer le modèle utilisateur défini
from django.contrib.auth import get_user_model

from django.utils.timezone import now

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('urgent_important', 'Urgent & Important'),
        ('important_not_urgent', 'Important mais pas Urgent'),
        ('urgent_not_important', 'Urgent mais pas Important'),
        ('not_urgent_not_important', 'Ni Urgent ni Important')
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    @property
    def urgent(self):
        """Détermine si la tâche est urgente"""
        return self.priority in ['urgent_important', 'urgent_not_important'] or self.due_date <= now()

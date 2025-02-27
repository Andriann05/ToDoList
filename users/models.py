from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # Change le related_name pour éviter le conflit
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users_permissions',  # Change aussi ici
        blank=True
    )
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        from PIL import Image
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            img.thumbnail((100, 100))
            img.save(self.avatar.path)

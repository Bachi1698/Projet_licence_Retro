from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profil(models.Model):
    email = models.EmailField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profil')
    email_confirmed = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=User)
    def create_user_profil(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profil(sender, instance, created, **kwargs):
        
        instance.user_profil.save()
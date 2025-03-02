from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Yeni istifadəçi qeydiyyatdan keçdikdə profil yaratmaq və bonus vermək
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Yeni istifadəçi yaradıldıqda profil yaradılır
        UserProfile.objects.create(user=instance, bonus=100.00)  # 100 AZN bonus əlavə edilir

# İstifadəçi profili yeniləndikdə bonusu yeniləmək üçün
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import assign_task_permissions

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'SUPERADMIN' if instance.is_superuser else 'USER'
        UserProfile.objects.create(user=instance, role=role)



@receiver(post_save, sender=UserProfile)
def update_user_permissions_on_role_change(sender, instance, **kwargs):
    user = instance.user
    role = instance.role

    if role == 'ADMIN':
        user.is_staff = True
        assign_task_permissions(user) 
    else:
        user.is_staff = False
        user.user_permissions.clear()
    
    user.save()

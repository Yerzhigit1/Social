from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Profile, User
import os
import logging

logger = logging.getLogger('users')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f'Создан профиль для пользователя {instance.email}')
        
        
@receiver(post_delete, sender=User)
def delete_profile_after_user_deleted(sender, instance, **kwargs):
    try:
        instance.profile.delete()
        logger.info(f'Удален профиль для пользователя {instance.email}')
    except Profile.DoesNotExist:
        logger.error(f'Профиль не существует {instance.email}')
        pass
        
        
@receiver(pre_save, sender=Profile)
def delete_old_files_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return
    
    if old_instance.avatar and old_instance.avatar != instance.avatar:
        if os.path.isfile(old_instance.avatar.path):
            try:
                os.remove(old_instance.avatar.path)
            except Exception:
                logger.error(f'Ошибка удаление старого аватара для {instance.email}')
    
    if old_instance.cover and old_instance.cover != instance.cover:
        if os.path.isfile(old_instance.cover.path):
            try:
                os.remove(old_instance.cover.path)
            except Exception:
                logger.error(f'Ошибка удаление старого кавера для {instance.email}')
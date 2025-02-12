
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Car, ChangeHistory,Fuell
from .middleware import get_current_user


@receiver(post_save, sender=Fuell)
@receiver(post_save, sender=Car)
def track_branch_creation_or_update(sender, instance, created, **kwargs):
    user = get_current_user()  # Kullanıcı bilgisini almak
    if created :
        if sender.__name__ == "Fuell":
            return 
        # Yeni bir nesne oluşturulmuşsa
        ChangeHistory.objects.create(
            model_name=sender.__name__,
            object_id=instance.pk,
            field_name='N/A',
            old_value=None,
            new_value=str(instance),
            change_type='create',
            user=user,
        )
        
    else:
        # Mevcut bir nesne güncelleniyorsa
        changes = instance._detect_changes(instance.__class__.objects.get(pk=instance.pk))
        for field, (old_value, new_value) in changes.items():
            ChangeHistory.objects.create(
                model_name=sender.__name__,
                object_id=instance.pk,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
                change_type='update',
                user=user,
            )


@receiver(post_delete, sender=Fuell)
@receiver(post_delete, sender=Car)
def track_branch_deletion(sender, instance, **kwargs):
    user = get_current_user()  
    if sender.__name__ == "Fuell":
        field_name = f"{(str(instance.pk))}-{instance.user}-{instance.contry}-{instance.kilometer}-{instance.liter}-{instance.delivery}-{str(instance.create_at)}"
    else:
        field_name =f"{instance.plate}-{instance.brand}-{instance.model}-{instance.vehicle_type}-{instance.debit}-{instance.title}-{instance.kilometer}-{instance.possession}-{instance.comment}-{instance.department}-{instance.contry}-{str(instance.create_at)}"
    ChangeHistory.objects.create(
        model_name=sender.__name__,
        object_id=instance.pk,
        field_name=field_name,
        old_value=str(instance),
        new_value=None,
        change_type='delete',
        user=user,
    )

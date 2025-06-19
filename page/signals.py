
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Car, ChangeHistory,Fuell,Notification   
from .middleware import get_current_user
from django.utils.timezone import now

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

@receiver(post_save, sender=Fuell)
def check_fuel_notifications(sender, instance, created, **kwargs):
    if not created:
        return  # sadece yeni kayıtlar için kontrol yap

    car = instance.car
    user = instance.user
    plate = car.plate

    try:
        average = float(instance.average)
    except (TypeError, ValueError):
        average = 0

    try:
        liter = float(instance.liter)
    except (TypeError, ValueError):
        liter = 0

    user_contry = user.contry
    car_contry = car.contry

    # 1. Ortalama yakıt 30'dan büyükse bildirim
    if average > 30:
        Notification.objects.create(
            user=user,
            message=f"{plate} plakalı araç km bilgileri yanlış girildi (ortalama yakıt {average:.2f} > 30).",
            created_at=now()
        )
    
    # 2. Ortalama yakıt 0'dan küçükse bildirim
    if average < 0:
        Notification.objects.create(
            user=user,
            message=f"{plate} plakalı araç km bilgileri yanlış girildi (ortalama yakıt {average:.2f} < 0).",
            created_at=now()
        )

    # 3. Litre 300'den fazla ise bildirim
    if liter > 300:
        Notification.objects.create(
            user=user,
            message=f"{plate} plakalı araç {liter} litre yakıt alımı yapmıştır.",
            created_at=now()
        )

    # 4. Yakıt alınan ilçe, araç kayıtlı ilçeden farklı ise bildirim
    if instance.contry != car_contry:
        Notification.objects.create(
            user=user,
            message=f"{plate} plakalı araç yakıt alımı {instance.contry} ilçesinde yapılmıştır (kayıtlı ilçe: {car_contry}).",
            created_at=now()
        )
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profil


@receiver(post_save, sender=Profil)
def profil_admin_huquqi(sender, instance, **kwargs):
    """O'qituvchi rolidagi profilga avtomatik admin panel huquqini beradi.

    rol='oqituvchi' bo'lsa -> user staff + superuser (admin panelga to'liq kiradi).
    rol boshqa bo'lsa -> admin huquqlari olib tashlanadi.
    """
    user = instance.user
    if not user:
        return

    oqituvchi = instance.rol == 'oqituvchi'

    # Faqat o'zgargan bo'lsa saqlaymiz (keraksiz yozuvlarni oldini olish)
    if user.is_staff != oqituvchi or user.is_superuser != oqituvchi:
        user.is_staff = oqituvchi
        user.is_superuser = oqituvchi
        user.save(update_fields=['is_staff', 'is_superuser'])

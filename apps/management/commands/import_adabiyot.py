"""Root papkadagi adabiyot PDF fayllarini media'ga joylab, Adabiyot yozuvlarini yaratadi."""
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.models import Adabiyot

# (root fayl nomi, ko'rinadigan nomi)
FAYLLAR = [
    ('adabiyot1.pdf', 'Geoaxborot texnologiyalari — 1-adabiyot'),
    ('adabiyot2.pdf', 'Geoaxborot texnologiyalari — 2-adabiyot'),
]


class Command(BaseCommand):
    help = "Root papkadagi adabiyot PDF fayllarini import qiladi"

    def handle(self, *args, **opts):
        media_root = str(settings.MEDIA_ROOT)
        dest_dir = os.path.join(media_root, 'adabiyotlar')
        os.makedirs(dest_dir, exist_ok=True)

        for i, (fname, nomi) in enumerate(FAYLLAR, 1):
            src = os.path.join(settings.BASE_DIR, fname)
            if not os.path.exists(src):
                self.stderr.write(self.style.WARNING('Topilmadi: %s' % fname))
                continue
            shutil.copy(src, os.path.join(dest_dir, fname))
            obj, created = Adabiyot.objects.update_or_create(
                fayl='adabiyotlar/%s' % fname,
                defaults={'nomi': nomi, 'tartib': i},
            )
            self.stdout.write(self.style.SUCCESS(
                '%s: %s' % (fname, 'qo\'shildi' if created else 'yangilandi')
            ))

        self.stdout.write(self.style.SUCCESS('Tayyor. Jami: %d' % Adabiyot.objects.count()))

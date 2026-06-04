"""Eski (matematika) kontentni o'chiradi.

Serverga deploy qilishda ishlatiladi: barcha Mavzu, Dars va Topshiriqlarni
(va ularga bog'liq Savol/Test natijalarni) o'chiradi. Keyin `import_gis`
ishga tushirilib, GIS kontenti qaytadan quriladi.

Foydalanish:
    python manage.py eski_kontent_tozalash --tasdiq
"""
from django.core.management.base import BaseCommand

from apps.models import Mavzu, Dars, Topshiriq


class Command(BaseCommand):
    help = "Eski Mavzu, Dars va Topshiriqlarni o'chiradi (deploy uchun)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--tasdiq', action='store_true',
            help="O'chirishni tasdiqlash (busiz faqat sanab ko'rsatadi)",
        )

    def handle(self, *args, **opts):
        m = Mavzu.objects.count()
        d = Dars.objects.count()
        t = Topshiriq.objects.count()

        self.stdout.write(f"Mavzu: {m} | Dars: {d} | Topshiriq: {t}")

        if not opts['tasdiq']:
            self.stdout.write(self.style.WARNING(
                "Hech narsa o'chirilmadi. O'chirish uchun: --tasdiq bilan ishlating."
            ))
            return

        t_res = Topshiriq.objects.all().delete()
        d_res = Dars.objects.all().delete()
        m_res = Mavzu.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            "O'chirildi:\n"
            f"  Topshiriq: {t_res}\n"
            f"  Dars: {d_res}\n"
            f"  Mavzu: {m_res}\n"
            "Endi `python manage.py import_gis --tozalash` ishga tushiring."
        ))

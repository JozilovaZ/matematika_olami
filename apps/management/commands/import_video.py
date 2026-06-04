"""GIS fani bo'yicha 10 ta video darsni (YouTube) bazaga joylaydi."""
from django.core.management.base import BaseCommand

from apps.models import VideoDars

# (youtube_id, nomi, tavsif)
VIDEOLAR = [
    ('7RUgLVVdfcQ', 'Geoaxborot tizimlari (GIS) — kirish',
     "GIS nima, uning komponentlari va qo'llanilish sohalari haqida umumiy tushuncha."),
    ('YSuRw6-kVuY', 'GISga amaliy kirish',
     "Geoaxborot tizimlari atamalari va asosiy tushunchalarining qisqacha amaliy sharhi."),
    ('NHolzMgaqwE', 'QGIS 3 — mutlaq boshlovchilar uchun qo\'llanma',
     "QGIS interfeysi va asosiy vositalari bilan tanishish."),
    ('pGm7w-LywO0', 'QGIS — to\'liq kirish kursi',
     "Xaritalash, fazoviy ma'lumotlarni qayta ishlash va tahlil — boshidan."),
    ('xKlk3IXyPMo', 'QGIS — keng qamrovli darslik',
     "Bepul va ochiq kodli QGIS dasturi bo'yicha to'liq kurs."),
    ('OOuq7BkUxc0', 'QGIS — boshlovchilar uchun (2025)',
     "Bosqichma-bosqich GIS amaliyoti: qatlamlar, atributlar, xaritalar."),
    ('BbUctneHfKc', 'ArcGIS Desktop — boshlovchilar uchun (1-qism)',
     "ArcGIS Desktop asoslari va geofazoviy ko'nikmalar."),
    ('FuRUZ_J5w9Y', 'ArcGIS — amaliy misollar bilan qo\'llanma',
     "Geoaxborot tizimlari asoslari amaliy misollar orqali."),
    ('qdkn82ruW0o', 'ArcGIS Pro — to\'liq boshlang\'ich kurs',
     "ArcGIS Pro: asosiydan ilg'or darajagacha."),
    ('n5evFcS0_1I', 'ArcGIS Pro — ishni boshlash',
     "ArcGIS Pro bilan loyiha yaratish va boshlang'ich sozlash."),
]


class Command(BaseCommand):
    help = "GIS bo'yicha 10 ta video darsni import qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--tozalash', action='store_true',
                            help="Avval mavjud video darslarni o'chiradi")

    def handle(self, *args, **opts):
        if opts.get('tozalash'):
            VideoDars.objects.all().delete()
            self.stdout.write("Eski video darslar o'chirildi.")

        for i, (yid, nomi, tavsif) in enumerate(VIDEOLAR, 1):
            VideoDars.objects.update_or_create(
                youtube_id=yid,
                defaults={'nomi': nomi, 'tavsif': tavsif, 'tartib': i},
            )
            self.stdout.write(self.style.SUCCESS('%d. %s' % (i, nomi)))

        self.stdout.write(self.style.SUCCESS('Tayyor. Jami: %d' % VideoDars.objects.count()))

from django.core.management.base import BaseCommand
from apps.models import Dars, Topshiriq, Savol


class Command(BaseCommand):
    help = "Har bir darsning oxiriga topshiriq va savollar qo'shadi"

    def handle(self, *args, **options):
        self.stdout.write("Dars testlari yuklanmoqda...")

        self._natural_sonlar()
        self._qoshish_ayirish()
        self._bolish()
        self._kasrlar()
        self._onli_kasrlar()
        self._foizlar()
        self._geometrik_shakllar()
        self._perimetr_yuza()

        self.stdout.write(self.style.SUCCESS("Barcha dars testlari muvaffaqiyatli yuklandi!"))

    def _top_qosh(self, dars, nomi, icon, rang, progress_rang, btn_rang):
        top, created = Topshiriq.objects.get_or_create(
            nomi=nomi,
            dars=dars,
            defaults={
                'icon': icon,
                'rang': rang,
                'progress_rang': progress_rang,
                'btn_rang': btn_rang,
                'turi': 'kichik',
                'tartib': Topshiriq.objects.filter(dars=dars).count(),
            }
        )
        if created:
            self.stdout.write(f"  + {dars.nomi}: '{nomi}' topshirig'i qo'shildi")
        return top, created

    def _savollar_qosh(self, top, savollar):
        if top.savollar_list.exists():
            return
        for i, s in enumerate(savollar):
            Savol.objects.create(topshiriq=top, tartib=i, **s)
        top.savollar = len(savollar)
        top.save(update_fields=['savollar'])

    def _natural_sonlar(self):
        dars = Dars.objects.filter(raqam='01').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Natural sonlar bo'yicha test",
            '🔢', '#e8f5e9', '#4caf50', '#4caf50'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': 'Quyidagilardan qaysi biri natural son?',
                'variant_a': '0', 'variant_b': '-5', 'variant_c': '7', 'variant_d': '1/2',
                'togri_javob': 'c',
                'izoh': 'Natural sonlar faqat musbat butun sonlar: 1, 2, 3, ... Javob: 7.',
            },
            {
                'savol_matni': '5 748 sonida yuzlar xonasidagi raqam qaysi?',
                'variant_a': '5', 'variant_b': '7', 'variant_c': '4', 'variant_d': '8',
                'togri_javob': 'b',
                'izoh': '5 748: minglar=5, yuzlar=7, o\'nlar=4, birlar=8.',
            },
            {
                'savol_matni': '3 472 sonini o\'nliklarcha yaxlitlang',
                'variant_a': '3 400', 'variant_b': '3 470', 'variant_c': '3 480', 'variant_d': '3 500',
                'togri_javob': 'b',
                'izoh': 'Birlar xonasi: 2 < 5, pastga yaxlitlanadi. 3 470.',
            },
            {
                'savol_matni': '9 876 va 9 867 ni taqqoslang',
                'variant_a': '9 876 < 9 867', 'variant_b': '9 876 = 9 867',
                'variant_c': '9 876 > 9 867', 'variant_d': 'Teng',
                'togri_javob': 'c',
                'izoh': 'O\'nlar xonasi: 7 > 6. Demak 9 876 > 9 867.',
            },
            {
                'savol_matni': '4 000 + 500 + 30 + 8 = ?',
                'variant_a': '4 358', 'variant_b': '4 538', 'variant_c': '4 583', 'variant_d': '5 438',
                'togri_javob': 'b',
                'izoh': 'Xonalar bo\'yicha: 4·1000 + 5·100 + 3·10 + 8 = 4 538.',
            },
            {
                'savol_matni': 'Bir xonali eng katta natural son qaysi?',
                'variant_a': '8', 'variant_b': '9', 'variant_c': '10', 'variant_d': '0',
                'togri_javob': 'b',
                'izoh': 'Bir xonali sonlar: 1 dan 9 gacha. Eng kattasi — 9.',
            },
            {
                'savol_matni': '10 000 dan kichik bo\'lgan eng katta natural son?',
                'variant_a': '9 000', 'variant_b': '9 009', 'variant_c': '9 990', 'variant_d': '9 999',
                'togri_javob': 'd',
                'izoh': '10 000 dan kichik eng katta son — 9 999.',
            },
            {
                'savol_matni': '6 050 sonini so\'z bilan ifodalang',
                'variant_a': 'Olti ming besh', 'variant_b': 'Olti ming ellik',
                'variant_c': 'Olti yuz ellik', 'variant_d': 'Olti ming besh yuz',
                'togri_javob': 'b',
                'izoh': '6 050 = 6 ming + 50 = "Olti ming ellik".',
            },
            {
                'savol_matni': '2, 4, 6, 8, ... ketma-ketlikda 10-had qaysi?',
                'variant_a': '18', 'variant_b': '20', 'variant_c': '22', 'variant_d': '16',
                'togri_javob': 'b',
                'izoh': 'Juft sonlar: n-had = 2n. 10-had = 2×10 = 20.',
            },
            {
                'savol_matni': '1 million necha xonali son?',
                'variant_a': '5', 'variant_b': '6', 'variant_c': '7', 'variant_d': '8',
                'togri_javob': 'c',
                'izoh': '1 000 000 — 7 ta raqamdan iborat, 7 xonali son.',
            },
        ])

    def _qoshish_ayirish(self):
        dars = Dars.objects.filter(raqam='02').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Qo'shish va ayirish testi",
            '➕', '#fff3e0', '#ff9800', '#ff9800'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': '348 + 152 = ?',
                'variant_a': '490', 'variant_b': '500', 'variant_c': '510', 'variant_d': '600',
                'togri_javob': 'b',
                'izoh': '348 + 152 = 500.',
            },
            {
                'savol_matni': '1 000 - 437 = ?',
                'variant_a': '573', 'variant_b': '563', 'variant_c': '463', 'variant_d': '673',
                'togri_javob': 'a',
                'izoh': '1 000 - 437 = 563. Tekshirish: 563 + 437 = 1 000.',
            },
            {
                'savol_matni': '2 456 + 3 544 = ?',
                'variant_a': '5 000', 'variant_b': '6 000', 'variant_c': '5 900', 'variant_d': '6 100',
                'togri_javob': 'b',
                'izoh': '2 456 + 3 544 = 6 000.',
            },
            {
                'savol_matni': '700 - 285 = ?',
                'variant_a': '415', 'variant_b': '405', 'variant_c': '425', 'variant_d': '515',
                'togri_javob': 'a',
                'izoh': '700 - 285 = 415.',
            },
            {
                'savol_matni': '999 + 1 001 = ?',
                'variant_a': '1 998', 'variant_b': '2 000', 'variant_c': '2 100', 'variant_d': '1 900',
                'togri_javob': 'b',
                'izoh': '999 + 1 001 = 2 000.',
            },
            {
                'savol_matni': '4 000 - 1 567 = ?',
                'variant_a': '2 433', 'variant_b': '2 533', 'variant_c': '3 433', 'variant_d': '2 333',
                'togri_javob': 'a',
                'izoh': '4 000 - 1 567 = 2 433.',
            },
            {
                'savol_matni': 'Qo\'shishning o\'rin almashtirish xossasi: 43 + 57 = ?',
                'variant_a': '43 + 57 = 100', 'variant_b': '57 + 43 = 100',
                'variant_c': 'Ikkisi ham to\'g\'ri', 'variant_d': 'Ikkisi ham noto\'g\'ri',
                'togri_javob': 'c',
                'izoh': 'a + b = b + a xossasi bo\'yicha 43+57 = 57+43 = 100.',
            },
            {
                'savol_matni': '235 + 127 + 165 = ?',
                'variant_a': '517', 'variant_b': '527', 'variant_c': '537', 'variant_d': '547',
                'togri_javob': 'b',
                'izoh': '235 + 165 = 400, keyin 400 + 127 = 527.',
            },
            {
                'savol_matni': 'Kutubxonada 1 250 ta kitob bor edi. 480 tasi berildi, 320 tasi qaytarildi. Nechta qoldi?',
                'variant_a': '1 090', 'variant_b': '1 090', 'variant_c': '1 090', 'variant_d': '1 090',
                'togri_javob': 'a',
                'izoh': '1 250 - 480 + 320 = 770 + 320 = 1 090 ta kitob.',
            },
            {
                'savol_matni': 'Ayirishni tekshirish uchun nima qilinadi?',
                'variant_a': 'Javobdan kamayuvchi ayiriladi',
                'variant_b': 'Javobga ayiruvchi qo\'shiladi',
                'variant_c': 'Javob ikkilanadi',
                'variant_d': 'Hech narsa qilinmaydi',
                'togri_javob': 'b',
                'izoh': 'Ayirmani tekshirish: ayirma + ayiruvchi = kamayuvchi bo\'lishi kerak.',
            },
        ])

    def _bolish(self):
        dars = Dars.objects.filter(raqam='04').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Bo'lish bo'yicha test",
            '➗', '#fce4ec', '#e91e63', '#e91e63'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': '48 ÷ 6 = ?',
                'variant_a': '6', 'variant_b': '7', 'variant_c': '8', 'variant_d': '9',
                'togri_javob': 'c',
                'izoh': '48 ÷ 6 = 8, chunki 6 × 8 = 48.',
            },
            {
                'savol_matni': '100 ÷ 25 = ?',
                'variant_a': '3', 'variant_b': '4', 'variant_c': '5', 'variant_d': '25',
                'togri_javob': 'b',
                'izoh': '100 ÷ 25 = 4.',
            },
            {
                'savol_matni': '29 ÷ 4 = ? (qoldiq bilan)',
                'variant_a': '7 qoldiq 1', 'variant_b': '6 qoldiq 5',
                'variant_c': '7 qoldiq 2', 'variant_d': '8 qoldiq 2',
                'togri_javob': 'a',
                'izoh': '4 × 7 = 28, 29 - 28 = 1. Javob: 7 qoldiq 1.',
            },
            {
                'savol_matni': '360 ÷ 9 = ?',
                'variant_a': '30', 'variant_b': '40', 'variant_c': '45', 'variant_d': '50',
                'togri_javob': 'b',
                'izoh': '360 ÷ 9 = 40.',
            },
            {
                'savol_matni': 'Qaysi son 2 ga bo\'linadi?',
                'variant_a': '37', 'variant_b': '43', 'variant_c': '56', 'variant_d': '81',
                'togri_javob': 'c',
                'izoh': '2 ga bo\'linadigan sonlar — oxirgi raqami juft: 56 ning oxiri 6 (juft).',
            },
            {
                'savol_matni': '126 soni 3 ga bo\'linadimi?',
                'variant_a': "Ha, bo'linadi", 'variant_b': "Yo'q, bo'linmaydi",
                'variant_c': "Qoldiq 1 bilan bo'linadi", 'variant_d': "Qoldiq 2 bilan bo'linadi",
                'togri_javob': 'a',
                'izoh': 'Raqamlar yig\'indisi: 1+2+6=9, 9÷3=3. Demak bo\'linadi.',
            },
            {
                'savol_matni': '0 ni har qanday songa bo\'lsak natija?',
                'variant_a': '1', 'variant_b': 'O\'sha son', 'variant_c': '0', 'variant_d': 'Aniqlanmagan',
                'togri_javob': 'c',
                'izoh': '0 ÷ n = 0 (har qanday n ≠ 0 uchun).',
            },
            {
                'savol_matni': '5 ga bo\'linadigan sonlar qanday tugaydi?',
                'variant_a': '1 yoki 5', 'variant_b': '0 yoki 5',
                'variant_c': '2 yoki 4', 'variant_d': '0 yoki 2',
                'togri_javob': 'b',
                'izoh': '5 ga bo\'linadigan sonlar 0 yoki 5 bilan tugaydi.',
            },
            {
                'savol_matni': '504 ÷ 7 = ?',
                'variant_a': '62', 'variant_b': '70', 'variant_c': '72', 'variant_d': '82',
                'togri_javob': 'c',
                'izoh': '7 × 72 = 504. Javob: 72.',
            },
            {
                'savol_matni': '120 ta shirin 8 bolaga teng taqsimlansa, har biriga nechtadan tegadi?',
                'variant_a': '12', 'variant_b': '15', 'variant_c': '16', 'variant_d': '20',
                'togri_javob': 'b',
                'izoh': '120 ÷ 8 = 15 ta shirin.',
            },
        ])

    def _kasrlar(self):
        dars = Dars.objects.filter(raqam='05').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Kasrlar bo'yicha test",
            '📊', '#f3e5f5', '#9c27b0', '#9c27b0'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': 'Kasr 3/5 da surat va maxraj qaysilar?',
                'variant_a': 'Surat=5, maxraj=3', 'variant_b': 'Surat=3, maxraj=5',
                'variant_c': 'Ikkalasi ham 3', 'variant_d': 'Ikkalasi ham 5',
                'togri_javob': 'b',
                'izoh': 'Kasr a/b: a — surat (yuqori), b — maxraj (pastki). 3/5 da surat=3, maxraj=5.',
            },
            {
                'savol_matni': '2/7 + 3/7 = ?',
                'variant_a': '5/14', 'variant_b': '5/7', 'variant_c': '6/7', 'variant_d': '1',
                'togri_javob': 'b',
                'izoh': 'Maxrajlar teng: (2+3)/7 = 5/7.',
            },
            {
                'savol_matni': '9/10 - 4/10 = ?',
                'variant_a': '5/20', 'variant_b': '13/10', 'variant_c': '5/10', 'variant_d': '4/10',
                'togri_javob': 'c',
                'izoh': '(9-4)/10 = 5/10.',
            },
            {
                'savol_matni': '1/4 + 1/2 = ?',
                'variant_a': '1/3', 'variant_b': '2/6', 'variant_c': '3/4', 'variant_d': '2/4',
                'togri_javob': 'c',
                'izoh': '1/2 = 2/4. Demak 1/4 + 2/4 = 3/4.',
            },
            {
                'savol_matni': '6/8 ni qisqartiring',
                'variant_a': '2/4', 'variant_b': '3/4', 'variant_c': '4/6', 'variant_d': '1/2',
                'togri_javob': 'b',
                'izoh': 'EKUB(6,8)=2. 6÷2=3, 8÷2=4. Javob: 3/4.',
            },
            {
                'savol_matni': '2/3 × 3/5 = ?',
                'variant_a': '6/15', 'variant_b': '5/8', 'variant_c': '2/5', 'variant_d': '6/8',
                'togri_javob': 'c',
                'izoh': '(2×3)/(3×5) = 6/15 = 2/5.',
            },
            {
                'savol_matni': '1/2 ÷ 1/4 = ?',
                'variant_a': '1/8', 'variant_b': '2', 'variant_c': '1/4', 'variant_d': '4',
                'togri_javob': 'b',
                'izoh': '1/2 ÷ 1/4 = 1/2 × 4/1 = 4/2 = 2.',
            },
            {
                'savol_matni': 'Qaysi kasr eng katta: 1/3, 1/4, 1/5, 1/2?',
                'variant_a': '1/3', 'variant_b': '1/4', 'variant_c': '1/5', 'variant_d': '1/2',
                'togri_javob': 'd',
                'izoh': 'Teng suratli kasrlarda maxraj kichik bo\'lsa, kasr katta. Maxraj 2 eng kichik.',
            },
            {
                'savol_matni': '2 butun 3/4 ni noto\'g\'ri kasrga aylantiring',
                'variant_a': '5/4', 'variant_b': '9/4', 'variant_c': '11/4', 'variant_d': '8/4',
                'togri_javob': 'c',
                'izoh': '2 × 4 + 3 = 11. Javob: 11/4.',
            },
            {
                'savol_matni': 'Bog\'da 40 ta daraxt bor. 3/8 qismi olma. Nechta olma daraxti?',
                'variant_a': '10', 'variant_b': '12', 'variant_c': '15', 'variant_d': '20',
                'togri_javob': 'c',
                'izoh': '40 × 3/8 = 120/8 = 15 ta olma daraxti.',
            },
        ])

    def _onli_kasrlar(self):
        dars = Dars.objects.filter(raqam='06').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "O'nli kasrlar testi",
            '🔣', '#e0f7fa', '#00bcd4', '#00bcd4'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': '0,3 ni oddiy kasrga aylantiring',
                'variant_a': '3/100', 'variant_b': '3/10', 'variant_c': '1/3', 'variant_d': '30/10',
                'togri_javob': 'b',
                'izoh': '0,3 = 3/10 (o\'ndan birlar xonasi).',
            },
            {
                'savol_matni': '1,25 + 2,75 = ?',
                'variant_a': '3,0', 'variant_b': '4,0', 'variant_c': '3,5', 'variant_d': '5,0',
                'togri_javob': 'b',
                'izoh': '1,25 + 2,75 = 4,00.',
            },
            {
                'savol_matni': '5,0 - 1,8 = ?',
                'variant_a': '2,2', 'variant_b': '3,2', 'variant_c': '4,2', 'variant_d': '3,8',
                'togri_javob': 'b',
                'izoh': '5,0 - 1,8 = 3,2.',
            },
            {
                'savol_matni': '0,4 × 0,5 = ?',
                'variant_a': '0,2', 'variant_b': '2,0', 'variant_c': '0,02', 'variant_d': '4,5',
                'togri_javob': 'a',
                'izoh': '4 × 5 = 20. Verguldan keyin 2 ta raqam → 0,20 = 0,2.',
            },
            {
                'savol_matni': '7,2 ÷ 4 = ?',
                'variant_a': '1,8', 'variant_b': '2,8', 'variant_c': '1,2', 'variant_d': '0,8',
                'togri_javob': 'a',
                'izoh': '7,2 ÷ 4 = 1,8.',
            },
            {
                'savol_matni': '3,14 sonida o\'ndan birlar xonasidagi raqam?',
                'variant_a': '3', 'variant_b': '4', 'variant_c': '1', 'variant_d': '0',
                'togri_javob': 'c',
                'izoh': '3,14: birlik=3, o\'ndan bir=1, yuzdan bir=4.',
            },
            {
                'savol_matni': 'Qaysi o\'nli kasr eng kichik: 0,8; 0,08; 0,18; 0,80?',
                'variant_a': '0,8', 'variant_b': '0,08', 'variant_c': '0,18', 'variant_d': '0,80',
                'togri_javob': 'b',
                'izoh': '0,08 < 0,18 < 0,8 = 0,80. Eng kichigi 0,08.',
            },
            {
                'savol_matni': '2 m 50 sm ni o\'nli kasr bilan ifodalang (metrda)',
                'variant_a': '2,5 m', 'variant_b': '25 m', 'variant_c': '0,25 m', 'variant_d': '250 m',
                'togri_javob': 'a',
                'izoh': '50 sm = 0,5 m. 2 m + 0,5 m = 2,5 m.',
            },
            {
                'savol_matni': '0,125 = ?/1000',
                'variant_a': '12', 'variant_b': '1 250', 'variant_c': '125', 'variant_d': '1,25',
                'togri_javob': 'c',
                'izoh': '0,125 = 125/1000 (mingdan birlar xonasigacha).',
            },
            {
                'savol_matni': 'Benzin narxi litr uchun 11,50 so\'m. 4 litr benzin qancha turadi?',
                'variant_a': '44,00', 'variant_b': '45,00', 'variant_c': '46,00', 'variant_d': '46,50',
                'togri_javob': 'c',
                'izoh': '11,50 × 4 = 46,00 so\'m.',
            },
        ])

    def _foizlar(self):
        dars = Dars.objects.filter(raqam='07').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Foizlar bo'yicha test",
            '💯', '#fff9c4', '#f9a825', '#f9a825'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': '1% necha qismga teng?',
                'variant_a': '1/10', 'variant_b': '1/100', 'variant_c': '1/1000', 'variant_d': '10/100',
                'togri_javob': 'b',
                'izoh': '1% = 1/100 = 0,01.',
            },
            {
                'savol_matni': '200 ning 10% i necha?',
                'variant_a': '10', 'variant_b': '20', 'variant_c': '200', 'variant_d': '2',
                'togri_javob': 'b',
                'izoh': '200 × 10 / 100 = 20.',
            },
            {
                'savol_matni': '50 ning 50% i necha?',
                'variant_a': '5', 'variant_b': '100', 'variant_c': '25', 'variant_d': '50',
                'togri_javob': 'c',
                'izoh': '50 × 50 / 100 = 25.',
            },
            {
                'savol_matni': 'Sinfda 40 o\'quvchi bor, 8 tasi yo\'q. Necha foizi yo\'q?',
                'variant_a': '8%', 'variant_b': '20%', 'variant_c': '25%', 'variant_d': '15%',
                'togri_javob': 'b',
                'izoh': '(8/40) × 100% = 20%.',
            },
            {
                'savol_matni': '100% nima degan ma\'no anglatadi?',
                'variant_a': 'Yarmini', 'variant_b': '100 marta ko\'p', 'variant_c': 'Butunni', 'variant_d': '100 ta',
                'togri_javob': 'c',
                'izoh': '100% = butun son (hammasi). 50% = yarmi.',
            },
            {
                'savol_matni': 'Kitob narxi 60 000 so\'m. 25% chegirmadan so\'ng qancha?',
                'variant_a': '15 000', 'variant_b': '40 000', 'variant_c': '45 000', 'variant_d': '50 000',
                'togri_javob': 'c',
                'izoh': 'Chegirma: 60 000 × 25/100 = 15 000. Narx: 60 000 - 15 000 = 45 000.',
            },
            {
                'savol_matni': '0,75 necha foizga teng?',
                'variant_a': '7,5%', 'variant_b': '75%', 'variant_c': '750%', 'variant_d': '0,75%',
                'togri_javob': 'b',
                'izoh': '0,75 = 75/100 = 75%.',
            },
            {
                'savol_matni': '30 ta savoldan 24 tasini to\'g\'ri yechdingiz. Necha foiz?',
                'variant_a': '70%', 'variant_b': '75%', 'variant_c': '80%', 'variant_d': '85%',
                'togri_javob': 'c',
                'izoh': '(24/30) × 100% = 80%.',
            },
            {
                'savol_matni': 'Narx 120 000 dan 150 000 ga ko\'tarildi. Necha foiz ko\'tarildi?',
                'variant_a': '20%', 'variant_b': '25%', 'variant_c': '30%', 'variant_d': '15%',
                'togri_javob': 'b',
                'izoh': 'O\'sish: 30 000. Foiz: (30 000/120 000) × 100% = 25%.',
            },
            {
                'savol_matni': '200 ga 15% qo\'shilsa, natija necha?',
                'variant_a': '215', 'variant_b': '220', 'variant_c': '225', 'variant_d': '230',
                'togri_javob': 'd',
                'izoh': '200 ning 15% = 30. 200 + 30 = 230.',
            },
        ])

    def _geometrik_shakllar(self):
        dars = Dars.objects.filter(raqam='08').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Geometrik shakllar testi",
            '📐', '#e8eaf6', '#5c6bc0', '#5c6bc0'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': 'Uchburchakning barcha burchaklari yig\'indisi necha gradus?',
                'variant_a': '90°', 'variant_b': '180°', 'variant_c': '270°', 'variant_d': '360°',
                'togri_javob': 'b',
                'izoh': 'Har qanday uchburchak burchaklari yig\'indisi = 180°.',
            },
            {
                'savol_matni': 'To\'g\'ri burchak necha gradus?',
                'variant_a': '45°', 'variant_b': '60°', 'variant_c': '90°', 'variant_d': '180°',
                'togri_javob': 'c',
                'izoh': 'To\'g\'ri burchak = 90°.',
            },
            {
                'savol_matni': 'Kvadratda nechta teng tomon bor?',
                'variant_a': '2', 'variant_b': '3', 'variant_c': '4', 'variant_d': '0',
                'togri_javob': 'c',
                'izoh': 'Kvadratda 4 ta tomon ham teng.',
            },
            {
                'savol_matni': 'Doiraning diametri 14 sm. Radiusi necha sm?',
                'variant_a': '28 sm', 'variant_b': '14 sm', 'variant_c': '7 sm', 'variant_d': '4 sm',
                'togri_javob': 'c',
                'izoh': 'r = d/2 = 14/2 = 7 sm.',
            },
            {
                'savol_matni': 'O\'tkir burchak nechanchi oraliqda yotadi?',
                'variant_a': '90° dan katta', 'variant_b': '0° dan 90° gacha',
                'variant_c': 'Aynan 90°', 'variant_d': '90° dan 180° gacha',
                'togri_javob': 'b',
                'izoh': 'O\'tkir burchak: 0° < α < 90°.',
            },
            {
                'savol_matni': 'Uchburchak burchaklari 60°, 70°. Uchinchi burchak?',
                'variant_a': '40°', 'variant_b': '50°', 'variant_c': '60°', 'variant_d': '70°',
                'togri_javob': 'b',
                'izoh': '180° - 60° - 70° = 50°.',
            },
            {
                'savol_matni': 'Teng tomonli uchburchak har bir burchagi necha gradus?',
                'variant_a': '45°', 'variant_b': '60°', 'variant_c': '90°', 'variant_d': '120°',
                'togri_javob': 'b',
                'izoh': '180° / 3 = 60°. Teng tomonli uchburchakda hamma burchaklar teng.',
            },
            {
                'savol_matni': 'To\'g\'ri to\'rtburchakning barcha burchaklari yig\'indisi?',
                'variant_a': '180°', 'variant_b': '270°', 'variant_c': '360°', 'variant_d': '90°',
                'togri_javob': 'c',
                'izoh': 'To\'rtburchak burchaklari yig\'indisi = 360°. To\'g\'ri to\'rtburchakda 4 × 90° = 360°.',
            },
            {
                'savol_matni': 'Romb va kvadratning farqi nima?',
                'variant_a': 'Rombda tomonlar teng emas', 'variant_b': 'Kvadratda burchaklar 90°, rombda emas',
                'variant_c': 'Rombda 3 tomon bor', 'variant_d': 'Farq yo\'q',
                'togri_javob': 'b',
                'izoh': 'Rombda ham barcha tomonlar teng, lekin burchaklar 90° emas. Kvadratda barchasi 90°.',
            },
            {
                'savol_matni': 'Doiraning markazi nima?',
                'variant_a': 'Doiraning eng uzun nuqtasi', 'variant_b': 'Doiraning tashqarisidagi nuqta',
                'variant_c': 'Doiraning barcha chekkalaridan teng masofada bo\'lgan nuqta', 'variant_d': 'Radius',
                'togri_javob': 'c',
                'izoh': 'Markaz — doiraning barcha chekka nuqtalaridan teng uzoqlikda joylashgan nuqta.',
            },
        ])

    def _perimetr_yuza(self):
        dars = Dars.objects.filter(raqam='09').first()
        if not dars:
            return
        top, created = self._top_qosh(
            dars, "Perimetr va yuza testi",
            '📏', '#efebe9', '#795548', '#795548'
        )
        self._savollar_qosh(top, [
            {
                'savol_matni': 'Kvadrat tomoni 6 sm. Perimetri?',
                'variant_a': '12 sm', 'variant_b': '18 sm', 'variant_c': '24 sm', 'variant_d': '36 sm',
                'togri_javob': 'c',
                'izoh': 'P = 4 × a = 4 × 6 = 24 sm.',
            },
            {
                'savol_matni': 'To\'g\'ri to\'rtburchak: a=8, b=5. Yuzasi?',
                'variant_a': '13 sm²', 'variant_b': '26 sm²', 'variant_c': '40 sm²', 'variant_d': '80 sm²',
                'togri_javob': 'c',
                'izoh': 'S = a × b = 8 × 5 = 40 sm².',
            },
            {
                'savol_matni': 'Uchburchak tomonlari 4, 7, 9 sm. Perimetri?',
                'variant_a': '18 sm', 'variant_b': '20 sm', 'variant_c': '22 sm', 'variant_d': '16 sm',
                'togri_javob': 'b',
                'izoh': 'P = 4 + 7 + 9 = 20 sm.',
            },
            {
                'savol_matni': 'Kvadrat yuzasi 81 sm². Tomoni necha sm?',
                'variant_a': '7 sm', 'variant_b': '8 sm', 'variant_c': '9 sm', 'variant_d': '11 sm',
                'togri_javob': 'c',
                'izoh': 'a = √81 = 9 sm.',
            },
            {
                'savol_matni': 'To\'g\'ri to\'rtburchak perimetri 28 sm, eni 6 sm. Bo\'yi?',
                'variant_a': '8 sm', 'variant_b': '16 sm', 'variant_c': '22 sm', 'variant_d': '14 sm',
                'togri_javob': 'a',
                'izoh': 'P = 2(a+b) → 28 = 2(6+b) → 14 = 6+b → b = 8 sm.',
            },
            {
                'savol_matni': 'Doira radiusi 3 sm. Yuzasi? (π ≈ 3)',
                'variant_a': '9 sm²', 'variant_b': '18 sm²', 'variant_c': '27 sm²', 'variant_d': '6 sm²',
                'togri_javob': 'c',
                'izoh': 'S = π × r² ≈ 3 × 9 = 27 sm².',
            },
            {
                'savol_matni': 'Uchburchak asosi 12 sm, balandligi 7 sm. Yuzasi?',
                'variant_a': '42 sm²', 'variant_b': '84 sm²', 'variant_c': '38 sm²', 'variant_d': '19 sm²',
                'togri_javob': 'a',
                'izoh': 'S = (a × h) / 2 = (12 × 7) / 2 = 42 sm².',
            },
            {
                'savol_matni': '1 dm² = necha sm²?',
                'variant_a': '10 sm²', 'variant_b': '100 sm²', 'variant_c': '1 000 sm²', 'variant_d': '10 000 sm²',
                'togri_javob': 'b',
                'izoh': '1 dm = 10 sm. 1 dm² = 10 × 10 = 100 sm².',
            },
            {
                'savol_matni': 'Xona 7m × 5m. Polga plitka uchun necha m² kerak?',
                'variant_a': '12 m²', 'variant_b': '24 m²', 'variant_c': '35 m²', 'variant_d': '70 m²',
                'togri_javob': 'c',
                'izoh': 'S = 7 × 5 = 35 m².',
            },
            {
                'savol_matni': 'Bog\' 30m × 20m. Atrofiga devor qurilsa, necha m devor kerak?',
                'variant_a': '50 m', 'variant_b': '100 m', 'variant_c': '600 m', 'variant_d': '300 m',
                'togri_javob': 'b',
                'izoh': 'Perimetr = 2(30 + 20) = 2 × 50 = 100 m.',
            },
        ])

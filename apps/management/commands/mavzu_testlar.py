from django.core.management.base import BaseCommand
from apps.models import Mavzu, Topshiriq, Savol


class Command(BaseCommand):
    help = "Har bir mavzu uchun testlar va savollar qo'shadi"

    def handle(self, *args, **options):
        self.stdout.write("Mavzu testlari yuklanmoqda...")

        self._natural_sonlar()
        self._kasrlar()
        self._geometriya()
        self._algebra()

        self.stdout.write(self.style.SUCCESS("Barcha mavzu testlari muvaffaqiyatli yuklandi!"))

    def _qosh_topshiriq(self, mavzu, nomi, icon, rang, progress_rang, btn_rang, turi='kichik'):
        top, created = Topshiriq.objects.get_or_create(
            nomi=nomi,
            mavzu=mavzu,
            defaults={
                'icon': icon,
                'rang': rang,
                'progress_rang': progress_rang,
                'btn_rang': btn_rang,
                'turi': turi,
                'tartib': Topshiriq.objects.filter(mavzu=mavzu).count(),
            }
        )
        if created:
            self.stdout.write(f"  + Topshiriq qo'shildi: {nomi}")
        return top, created

    def _qosh_savollar(self, top, savollar):
        if top.savollar_list.exists():
            return
        for i, s in enumerate(savollar):
            Savol.objects.create(topshiriq=top, tartib=i, **s)
        top.savollar = len(savollar)
        top.save(update_fields=['savollar'])

    def _natural_sonlar(self):
        mavzu = Mavzu.objects.filter(raqam='01').first()
        if not mavzu:
            self.stdout.write("Natural sonlar mavzusi topilmadi!")
            return

        # Test 1: Sonlarni taqqoslash va yaxlitlash
        top, created = self._qosh_topshiriq(
            mavzu, "Natural sonlar testi",
            '🔢', '#e8f5e9', '#4caf50', '#4caf50'
        )
        self._qosh_savollar(top, [
            {
                'savol_matni': 'Quyidagi sonlardan qaysi biri natural son emas?',
                'variant_a': '1', 'variant_b': '100', 'variant_c': '0', 'variant_d': '999',
                'togri_javob': 'c',
                'izoh': '0 (nol) natural son emas. Natural sonlar 1 dan boshlanadi.',
            },
            {
                'savol_matni': '3 826 sonida minglar xonasidagi raqam qaysi?',
                'variant_a': '8', 'variant_b': '2', 'variant_c': '6', 'variant_d': '3',
                'togri_javob': 'd',
                'izoh': '3 826 = 3·1000 + 8·100 + 2·10 + 6. Minglar xonasida 3 turibdi.',
            },
            {
                'savol_matni': '4 753 sonini yuzliklargacha yaxlitlang',
                'variant_a': '4 700', 'variant_b': '4 800', 'variant_c': '5 000', 'variant_d': '4 750',
                'togri_javob': 'b',
                'izoh': "O'nliklar xonasidagi raqam 5 ≥ 5, shuning uchun yuqoriga yaxlitlanadi: 4 800.",
            },
            {
                'savol_matni': '5 284 va 5 248 sonlarini taqqoslang',
                'variant_a': '5 284 < 5 248', 'variant_b': '5 284 = 5 248',
                'variant_c': '5 284 > 5 248', 'variant_d': 'Aytib bo\'lmaydi',
                'togri_javob': 'c',
                'izoh': 'Minglik va yuzlik xonalar teng. O\'nliklar: 8 > 4. Demak 5 284 > 5 248.',
            },
            {
                'savol_matni': '2 000 + 300 + 40 + 7 = ?',
                'variant_a': '2 347', 'variant_b': '2 374', 'variant_c': '2 437', 'variant_d': '2 473',
                'togri_javob': 'a',
                'izoh': 'Xonalar bo\'yicha yig\'indisi: 2·1000 + 3·100 + 4·10 + 7 = 2 347.',
            },
            {
                'savol_matni': '7 203 sonini so\'z bilan ifodalang',
                'variant_a': 'Yetti yuz uch', 'variant_b': 'Yetti ming ikki yuz uch',
                'variant_c': 'Yetti ming yigirma uch', 'variant_d': 'Yetti ikki nol uch',
                'togri_javob': 'b',
                'izoh': '7 203 = 7 ming 2 yuz 3. "Yetti ming ikki yuz uch" deb o\'qiladi.',
            },
            {
                'savol_matni': '9 999 dan keyin qaysi son keladi?',
                'variant_a': '9 998', 'variant_b': '10 000', 'variant_c': '9 990', 'variant_d': '10 001',
                'togri_javob': 'b',
                'izoh': '9 999 + 1 = 10 000.',
            },
            {
                'savol_matni': '6 050 sonini tahlil qiling: o\'nliklar xonasidagi raqam?',
                'variant_a': '6', 'variant_b': '0', 'variant_c': '5', 'variant_d': '50',
                'togri_javob': 'c',
                'izoh': '6 050: minglar=6, yuzlar=0, o\'nlar=5, birlar=0. O\'nliklar xonasida 5.',
            },
            {
                'savol_matni': '1 000 000 (bir million) necha xonali son?',
                'variant_a': '5', 'variant_b': '6', 'variant_c': '7', 'variant_d': '8',
                'togri_javob': 'c',
                'izoh': '1 000 000 da 7 ta raqam bor, demak u 7 xonali son.',
            },
            {
                'savol_matni': 'Uch xonali eng katta natural sonni toping',
                'variant_a': '100', 'variant_b': '900', 'variant_c': '990', 'variant_d': '999',
                'togri_javob': 'd',
                'izoh': 'Uch xonali sonlar 100 dan 999 gacha. Eng kattasi 999.',
            },
        ])

        # Test 2: Sonlar ketma-ketligi va qonuniyatlari
        top2, created2 = self._qosh_topshiriq(
            mavzu, "Sonlar ketma-ketligi",
            '📈', '#e8f5e9', '#43a047', '#43a047'
        )
        self._qosh_savollar(top2, [
            {
                'savol_matni': '2, 4, 6, 8, ... — keyingi son?',
                'variant_a': '9', 'variant_b': '10', 'variant_c': '12', 'variant_d': '11',
                'togri_javob': 'b',
                'izoh': 'Juft sonlar ketma-ketligi: har safar 2 qo\'shiladi. 8 + 2 = 10.',
            },
            {
                'savol_matni': '100, 90, 80, 70, ... — keyingi son?',
                'variant_a': '65', 'variant_b': '55', 'variant_c': '60', 'variant_d': '50',
                'togri_javob': 'c',
                'izoh': 'Har safar 10 ayirilmoqda. 70 - 10 = 60.',
            },
            {
                'savol_matni': '1, 3, 5, 7, ... — bu qanday sonlar ketma-ketligi?',
                'variant_a': 'Juft sonlar', 'variant_b': 'Toq sonlar',
                'variant_c': 'Kasr sonlar', 'variant_d': 'Manfiy sonlar',
                'togri_javob': 'b',
                'izoh': '1, 3, 5, 7 — bular toq sonlar (juft sonlarga bo\'linmaydigan natural sonlar).',
            },
            {
                'savol_matni': '5, 10, 15, 20, ... — keyingi uchta son?',
                'variant_a': '25, 30, 35', 'variant_b': '23, 26, 29',
                'variant_c': '21, 22, 23', 'variant_d': '30, 40, 50',
                'togri_javob': 'a',
                'izoh': '5 ning karralilari ketma-ketligi. 20 + 5 = 25, 25 + 5 = 30, 30 + 5 = 35.',
            },
            {
                'savol_matni': '1 dan 10 gacha natural sonlar yig\'indisi necha?',
                'variant_a': '45', 'variant_b': '50', 'variant_c': '55', 'variant_d': '60',
                'togri_javob': 'c',
                'izoh': '1+2+3+4+5+6+7+8+9+10 = 55. Formula: n(n+1)/2 = 10×11/2 = 55.',
            },
            {
                'savol_matni': 'Qaysi son 2 ga ham, 5 ga ham bo\'linadi?',
                'variant_a': '12', 'variant_b': '25', 'variant_c': '30', 'variant_d': '14',
                'togri_javob': 'c',
                'izoh': '30: 30÷2=15 ✓, 30÷5=6 ✓. 10 ning karralilari 2 va 5 ga bo\'linadi.',
            },
            {
                'savol_matni': '50 dan kichik juft sonlar nechtadan?',
                'variant_a': '24', 'variant_b': '25', 'variant_c': '26', 'variant_d': '20',
                'togri_javob': 'a',
                'izoh': '2, 4, 6, ..., 48 — bu 24 ta juft son (48÷2=24).',
            },
            {
                'savol_matni': '1, 4, 9, 16, 25, ... — keyingi son?',
                'variant_a': '30', 'variant_b': '35', 'variant_c': '36', 'variant_d': '49',
                'togri_javob': 'c',
                'izoh': 'Bu to\'liq kvadratlar: 1²=1, 2²=4, 3²=9, 4²=16, 5²=25, 6²=36.',
            },
            {
                'savol_matni': '100 dan 200 gacha nechta son bor? (100 va 200 ni ham sanang)',
                'variant_a': '99', 'variant_b': '100', 'variant_c': '101', 'variant_d': '200',
                'togri_javob': 'c',
                'izoh': '200 - 100 + 1 = 101 ta son (ikki chegarani ham qo\'shamiz).',
            },
            {
                'savol_matni': 'Natural sonlar qatoridagi eng kichik son qaysi?',
                'variant_a': '0', 'variant_b': '-1', 'variant_c': '1', 'variant_d': '2',
                'togri_javob': 'c',
                'izoh': 'Natural sonlar 1 dan boshlanadi. Eng kichigi — 1.',
            },
        ])

    def _kasrlar(self):
        mavzu = Mavzu.objects.filter(raqam='02').first()
        if not mavzu:
            self.stdout.write("Kasrlar mavzusi topilmadi!")
            return

        top, created = self._qosh_topshiriq(
            mavzu, "Kasrlar testi",
            '📊', '#fff3e0', '#ff9800', '#ff9800'
        )
        self._qosh_savollar(top, [
            {
                'savol_matni': 'Pitsa 6 ga bo\'lingan, 2 tasini yedingiz. Bu qanday kasr?',
                'variant_a': '1/3', 'variant_b': '2/6', 'variant_c': '2/4', 'variant_d': 'A va B to\'g\'ri',
                'togri_javob': 'd',
                'izoh': '2/6 = 1/3 (qisqartirilganda). Ikkisi ham to\'g\'ri ifoda.',
            },
            {
                'savol_matni': '3/4 va 2/3 dan qaysi biri katta?',
                'variant_a': '2/3', 'variant_b': '3/4', 'variant_c': 'Teng', 'variant_d': 'Aytib bo\'lmaydi',
                'togri_javob': 'b',
                'izoh': '3/4 = 0,75; 2/3 ≈ 0,67. Demak 3/4 > 2/3.',
            },
            {
                'savol_matni': '5/8 + 1/8 = ?',
                'variant_a': '6/16', 'variant_b': '4/8', 'variant_c': '6/8', 'variant_d': '5/8',
                'togri_javob': 'c',
                'izoh': 'Maxrajlar teng: 5/8 + 1/8 = (5+1)/8 = 6/8.',
            },
            {
                'savol_matni': '7/10 - 3/10 = ?',
                'variant_a': '4/20', 'variant_b': '4/0', 'variant_c': '10/10', 'variant_d': '4/10',
                'togri_javob': 'd',
                'izoh': 'Maxrajlar teng: 7/10 - 3/10 = (7-3)/10 = 4/10.',
            },
            {
                'savol_matni': '1/2 + 1/4 = ?',
                'variant_a': '2/6', 'variant_b': '2/4', 'variant_c': '3/4', 'variant_d': '1/4',
                'togri_javob': 'c',
                'izoh': 'Umumiy maxraj 4: 1/2 = 2/4. Demak 2/4 + 1/4 = 3/4.',
            },
            {
                'savol_matni': '4/6 ni qisqartiring',
                'variant_a': '1/2', 'variant_b': '2/3', 'variant_c': '3/4', 'variant_d': '2/4',
                'togri_javob': 'b',
                'izoh': 'EKUB(4,6) = 2. 4÷2=2, 6÷2=3. Javob: 2/3.',
            },
            {
                'savol_matni': '1/3 × 1/3 = ?',
                'variant_a': '2/3', 'variant_b': '1/9', 'variant_c': '2/9', 'variant_d': '1/6',
                'togri_javob': 'b',
                'izoh': 'Kasrlarni ko\'paytirish: 1/3 × 1/3 = (1×1)/(3×3) = 1/9.',
            },
            {
                'savol_matni': '3/4 ÷ 3/8 = ?',
                'variant_a': '9/32', 'variant_b': '1/2', 'variant_c': '2', 'variant_d': '6/4',
                'togri_javob': 'c',
                'izoh': 'Bo\'lishda teskari kasrga ko\'paytiramiz: 3/4 × 8/3 = 24/12 = 2.',
            },
            {
                'savol_matni': '1 butun 1/2 ni kasrga aylantiring',
                'variant_a': '2/2', 'variant_b': '3/2', 'variant_c': '1/2', 'variant_d': '4/2',
                'togri_javob': 'b',
                'izoh': '1 butun 1/2 = 1 + 1/2 = 2/2 + 1/2 = 3/2.',
            },
            {
                'savol_matni': 'Sinfda 30 o\'quvchi bor. 1/3 qismi qiz. Nechta qiz?',
                'variant_a': '3', 'variant_b': '13', 'variant_c': '10', 'variant_d': '15',
                'togri_javob': 'c',
                'izoh': '30 ning 1/3 qismi = 30 ÷ 3 = 10 ta qiz.',
            },
        ])

        top2, created2 = self._qosh_topshiriq(
            mavzu, "O'nli kasrlar testi",
            '🔣', '#fff3e0', '#ffa726', '#ffa726'
        )
        self._qosh_savollar(top2, [
            {
                'savol_matni': '0,5 ni oddiy kasrga aylantiring',
                'variant_a': '5/100', 'variant_b': '1/5', 'variant_c': '1/2', 'variant_d': '5/10',
                'togri_javob': 'c',
                'izoh': '0,5 = 5/10 = 1/2 (qisqartirilganda).',
            },
            {
                'savol_matni': '2,3 + 1,7 = ?',
                'variant_a': '3,0', 'variant_b': '4,0', 'variant_c': '3,10', 'variant_d': '5,0',
                'togri_javob': 'b',
                'izoh': 'Vergullarni tekislab qo\'shamiz: 2,3 + 1,7 = 4,0.',
            },
            {
                'savol_matni': '5,6 - 2,8 = ?',
                'variant_a': '2,2', 'variant_b': '3,2', 'variant_c': '2,8', 'variant_d': '3,8',
                'togri_javob': 'c',
                'izoh': '5,6 - 2,8 = 2,8.',
            },
            {
                'savol_matni': '0,1 × 0,1 = ?',
                'variant_a': '0,1', 'variant_b': '0,2', 'variant_c': '0,01', 'variant_d': '1,0',
                'togri_javob': 'c',
                'izoh': '1 × 1 = 1. Verguldan keyin jami 2 ta raqam → 0,01.',
            },
            {
                'savol_matni': '3,14 sonida yuzdan birlar xonasidagi raqam?',
                'variant_a': '3', 'variant_b': '1', 'variant_c': '4', 'variant_d': '0',
                'togri_javob': 'c',
                'izoh': '3,14: birliklar=3, o\'ndan birlar=1, yuzdan birlar=4.',
            },
            {
                'savol_matni': '1,5 × 2 = ?',
                'variant_a': '2,5', 'variant_b': '3,5', 'variant_c': '3,0', 'variant_d': '2,0',
                'togri_javob': 'c',
                'izoh': '1,5 × 2 = 3,0. Yoki: 15 × 2 = 30, verguldan 1 ta raqam → 3,0.',
            },
            {
                'savol_matni': '0,75 = ?/100',
                'variant_a': '7', 'variant_b': '750', 'variant_c': '7,5', 'variant_d': '75',
                'togri_javob': 'd',
                'izoh': '0,75 = 75/100.',
            },
            {
                'savol_matni': 'Qaysi o\'nli kasr eng katta: 0,9; 0,09; 0,99; 0,909?',
                'variant_a': '0,9', 'variant_b': '0,09', 'variant_c': '0,99', 'variant_d': '0,909',
                'togri_javob': 'c',
                'izoh': 'O\'ndan birlar: 0,99 da o\'ndan bir = 9 va yuzdan bir = 9. Eng kattasi 0,99.',
            },
            {
                'savol_matni': '4,8 ÷ 2 = ?',
                'variant_a': '2,4', 'variant_b': '2,8', 'variant_c': '2,0', 'variant_d': '4,0',
                'togri_javob': 'a',
                'izoh': '4,8 ÷ 2 = 2,4.',
            },
            {
                'savol_matni': '2,5 m ni sm ga aylantiring',
                'variant_a': '25 sm', 'variant_b': '250 sm', 'variant_c': '2500 sm', 'variant_d': '0,025 sm',
                'togri_javob': 'b',
                'izoh': '1 m = 100 sm. 2,5 m = 2,5 × 100 = 250 sm.',
            },
        ])

    def _geometriya(self):
        mavzu = Mavzu.objects.filter(raqam='03').first()
        if not mavzu:
            self.stdout.write("Geometriya mavzusi topilmadi!")
            return

        top, created = self._qosh_topshiriq(
            mavzu, "Geometrik shakllar testi",
            '📐', '#e3f2fd', '#2196f3', '#2196f3'
        )
        self._qosh_savollar(top, [
            {
                'savol_matni': 'To\'g\'ri to\'rtburchakning tomonlari a=7 sm, b=4 sm. Perimetri?',
                'variant_a': '11 sm', 'variant_b': '22 sm', 'variant_c': '28 sm', 'variant_d': '44 sm',
                'togri_javob': 'b',
                'izoh': 'P = 2(a + b) = 2(7 + 4) = 2 × 11 = 22 sm.',
            },
            {
                'savol_matni': 'Kvadratning tomoni 9 sm. Yuzasi necha sm²?',
                'variant_a': '18', 'variant_b': '36', 'variant_c': '81', 'variant_d': '72',
                'togri_javob': 'c',
                'izoh': 'S = a² = 9² = 81 sm².',
            },
            {
                'savol_matni': 'Uchburchakning burchaklari 40° va 75°. Uchinchi burchak?',
                'variant_a': '55°', 'variant_b': '65°', 'variant_c': '75°', 'variant_d': '115°',
                'togri_javob': 'b',
                'izoh': '180° - 40° - 75° = 65°.',
            },
            {
                'savol_matni': 'Doiraning radiusi 6 sm. Diametri necha sm?',
                'variant_a': '3 sm', 'variant_b': '6 sm', 'variant_c': '12 sm', 'variant_d': '36 sm',
                'togri_javob': 'c',
                'izoh': 'd = 2r = 2 × 6 = 12 sm.',
            },
            {
                'savol_matni': 'To\'g\'ri to\'rtburchakning tomonlari 5 sm va 8 sm. Yuzasi?',
                'variant_a': '26 sm²', 'variant_b': '40 sm²', 'variant_c': '13 sm²', 'variant_d': '80 sm²',
                'togri_javob': 'b',
                'izoh': 'S = a × b = 5 × 8 = 40 sm².',
            },
            {
                'savol_matni': 'Uchburchak asosi 10 sm, balandligi 6 sm. Yuzasi?',
                'variant_a': '16 sm²', 'variant_b': '60 sm²', 'variant_c': '30 sm²', 'variant_d': '120 sm²',
                'togri_javob': 'c',
                'izoh': 'S = (a × h) / 2 = (10 × 6) / 2 = 30 sm².',
            },
            {
                'savol_matni': 'Barcha tomonlari 4 sm ga teng uchburchak qanday uchburchak?',
                'variant_a': 'Teng yonli', 'variant_b': 'To\'g\'ri burchakli',
                'variant_c': 'Teng tomonli', 'variant_d': 'O\'tkir burchakli',
                'togri_javob': 'c',
                'izoh': 'Barcha uch tomoni teng bo\'lgan uchburchak — teng tomonli uchburchak.',
            },
            {
                'savol_matni': "Xona o'lchamlari 6 m × 4 m. Polga gilam yotqizish uchun necha m² kerak?",
                'variant_a': '10 m²', 'variant_b': '20 m²', 'variant_c': '24 m²', 'variant_d': '48 m²',
                'togri_javob': 'c',
                'izoh': 'S = 6 × 4 = 24 m².',
            },
            {
                'savol_matni': 'Kvadratning perimetri 36 sm. Tomoni necha sm?',
                'variant_a': '6 sm', 'variant_b': '9 sm', 'variant_c': '12 sm', 'variant_d': '4 sm',
                'togri_javob': 'b',
                'izoh': 'P = 4a → a = P ÷ 4 = 36 ÷ 4 = 9 sm.',
            },
            {
                'savol_matni': 'Doiraning yuzasini hisoblash formulasi?',
                'variant_a': 'S = 2πr', 'variant_b': 'S = πr²', 'variant_c': 'S = πd', 'variant_d': 'S = 2πr²',
                'togri_javob': 'b',
                'izoh': 'Doira yuzasi S = πr² ≈ 3,14 × r².',
            },
        ])

        top2, created2 = self._qosh_topshiriq(
            mavzu, "Perimetr va yuza testi",
            '📏', '#e3f2fd', '#1976d2', '#1976d2'
        )
        self._qosh_savollar(top2, [
            {
                'savol_matni': 'To\'g\'ri to\'rtburchakning yuzasi 48 sm², eni 6 sm. Bo\'yi?',
                'variant_a': '6 sm', 'variant_b': '8 sm', 'variant_c': '42 sm', 'variant_d': '10 sm',
                'togri_javob': 'b',
                'izoh': 'S = a × b → b = S ÷ a = 48 ÷ 6 = 8 sm.',
            },
            {
                'savol_matni': 'Kvadratning yuzasi 64 sm². Perimetri?',
                'variant_a': '16 sm', 'variant_b': '32 sm', 'variant_c': '8 sm', 'variant_d': '64 sm',
                'togri_javob': 'b',
                'izoh': 'a = √64 = 8 sm. P = 4 × 8 = 32 sm.',
            },
            {
                'savol_matni': 'Uchburchak tomonlari 5 sm, 7 sm, 9 sm. Perimetri?',
                'variant_a': '19 sm', 'variant_b': '21 sm', 'variant_c': '63 sm', 'variant_d': '35 sm',
                'togri_javob': 'b',
                'izoh': 'P = a + b + c = 5 + 7 + 9 = 21 sm.',
            },
            {
                'savol_matni': 'Doiraning radiusi 5 sm. Aylana uzunligi? (π ≈ 3,14)',
                'variant_a': '31,4 sm', 'variant_b': '15,7 sm', 'variant_c': '78,5 sm', 'variant_d': '10 sm',
                'togri_javob': 'a',
                'izoh': 'C = 2πr = 2 × 3,14 × 5 = 31,4 sm.',
            },
            {
                'savol_matni': 'Bog\' 20 m × 15 m. Atrofiga panjara qurilsa, necha m panjara kerak?',
                'variant_a': '35 m', 'variant_b': '70 m', 'variant_c': '300 m', 'variant_d': '150 m',
                'togri_javob': 'b',
                'izoh': 'Perimetr = 2(20 + 15) = 2 × 35 = 70 m.',
            },
            {
                'savol_matni': '1 m² necha sm²?',
                'variant_a': '100 sm²', 'variant_b': '1 000 sm²', 'variant_c': '10 000 sm²', 'variant_d': '1 000 000 sm²',
                'togri_javob': 'c',
                'izoh': '1 m = 100 sm. 1 m² = 100 sm × 100 sm = 10 000 sm².',
            },
            {
                'savol_matni': 'Teng tomonli uchburchak tomoni 8 sm. Perimetri?',
                'variant_a': '16 sm', 'variant_b': '24 sm', 'variant_c': '32 sm', 'variant_d': '64 sm',
                'togri_javob': 'b',
                'izoh': 'Teng tomonli uchburchakda P = 3 × a = 3 × 8 = 24 sm.',
            },
            {
                'savol_matni': 'To\'g\'ri to\'rtburchakning perimetri 26 sm, eni 5 sm. Bo\'yi?',
                'variant_a': '8 sm', 'variant_b': '16 sm', 'variant_c': '21 sm', 'variant_d': '13 sm',
                'togri_javob': 'a',
                'izoh': 'P = 2(a + b) → 26 = 2(5 + b) → 13 = 5 + b → b = 8 sm.',
            },
            {
                'savol_matni': 'Xona devorini bo\'yash uchun yuza yoki perimetr hisoblanadimi?',
                'variant_a': 'Perimetr', 'variant_b': 'Yuza', 'variant_c': 'Diametr', 'variant_d': 'Radius',
                'togri_javob': 'b',
                'izoh': 'Devor bo\'yash uchun devolning yuzasi (m²) hisoblanadi, chunki bo\'yoq miqdori yuzaga bog\'liq.',
            },
            {
                'savol_matni': 'Ikki kvadratning tomonlari 3 sm va 5 sm. Ularning yuzalari yig\'indisi?',
                'variant_a': '15 sm²', 'variant_b': '34 sm²', 'variant_c': '64 sm²', 'variant_d': '16 sm²',
                'togri_javob': 'b',
                'izoh': '3² + 5² = 9 + 25 = 34 sm².',
            },
        ])

    def _algebra(self):
        mavzu = Mavzu.objects.filter(raqam='04').first()
        if not mavzu:
            self.stdout.write("Algebra mavzusi topilmadi!")
            return

        top, created = self._qosh_topshiriq(
            mavzu, "Tenglamalar testi",
            '📝', '#fce4ec', '#e91e63', '#e91e63'
        )
        self._qosh_savollar(top, [
            {
                'savol_matni': 'x + 5 = 12. x = ?',
                'variant_a': '5', 'variant_b': '7', 'variant_c': '17', 'variant_d': '60',
                'togri_javob': 'b',
                'izoh': 'x = 12 - 5 = 7.',
            },
            {
                'savol_matni': '3x = 21. x = ?',
                'variant_a': '6', 'variant_b': '7', 'variant_c': '8', 'variant_d': '63',
                'togri_javob': 'b',
                'izoh': 'x = 21 ÷ 3 = 7.',
            },
            {
                'savol_matni': 'x - 8 = 15. x = ?',
                'variant_a': '7', 'variant_b': '120', 'variant_c': '23', 'variant_d': '13',
                'togri_javob': 'c',
                'izoh': 'x = 15 + 8 = 23.',
            },
            {
                'savol_matni': 'x ÷ 4 = 9. x = ?',
                'variant_a': '5', 'variant_b': '13', 'variant_c': '2,25', 'variant_d': '36',
                'togri_javob': 'd',
                'izoh': 'x = 9 × 4 = 36.',
            },
            {
                'savol_matni': '2x + 3 = 11. x = ?',
                'variant_a': '3', 'variant_b': '4', 'variant_c': '5', 'variant_d': '7',
                'togri_javob': 'b',
                'izoh': '2x = 11 - 3 = 8, x = 8 ÷ 2 = 4.',
            },
            {
                'savol_matni': '5x - 10 = 20. x = ?',
                'variant_a': '2', 'variant_b': '6', 'variant_c': '4', 'variant_d': '30',
                'togri_javob': 'b',
                'izoh': '5x = 20 + 10 = 30, x = 30 ÷ 5 = 6.',
            },
            {
                'savol_matni': 'a = 4 bo\'lsa, 3a + 2 = ?',
                'variant_a': '9', 'variant_b': '14', 'variant_c': '18', 'variant_d': '24',
                'togri_javob': 'b',
                'izoh': '3 × 4 + 2 = 12 + 2 = 14.',
            },
            {
                'savol_matni': 'Bir songa 7 qo\'shildi va natija 15 bo\'ldi. Bu son qaysi?',
                'variant_a': '22', 'variant_b': '8', 'variant_c': '105', 'variant_d': '6',
                'togri_javob': 'b',
                'izoh': 'x + 7 = 15, x = 15 - 7 = 8.',
            },
            {
                'savol_matni': 'x > 5 va x < 10 bo\'lgan butun sonlar nechtadan?',
                'variant_a': '3', 'variant_b': '4', 'variant_c': '5', 'variant_d': '6',
                'togri_javob': 'b',
                'izoh': '5 < x < 10 shartiga mos butun sonlar: 6, 7, 8, 9 — jami 4 ta.',
            },
            {
                'savol_matni': '4(x + 2) = 20. x = ?',
                'variant_a': '3', 'variant_b': '5', 'variant_c': '18', 'variant_d': '4',
                'togri_javob': 'a',
                'izoh': 'x + 2 = 20 ÷ 4 = 5, x = 5 - 2 = 3.',
            },
        ])

        top2, created2 = self._qosh_topshiriq(
            mavzu, "Tengsizliklar va ifodalar",
            '🔍', '#fce4ec', '#c2185b', '#c2185b'
        )
        self._qosh_savollar(top2, [
            {
                'savol_matni': 'x = 3 bo\'lsa, 2x² - 1 = ?',
                'variant_a': '11', 'variant_b': '17', 'variant_c': '35', 'variant_d': '5',
                'togri_javob': 'b',
                'izoh': '2 × 3² - 1 = 2 × 9 - 1 = 18 - 1 = 17.',
            },
            {
                'savol_matni': 'Qaysi qiymat 3x < 15 tengsizligini qoniqtiradi?',
                'variant_a': '5', 'variant_b': '6', 'variant_c': '4', 'variant_d': '7',
                'togri_javob': 'c',
                'izoh': '3 × 4 = 12 < 15 ✓. Boshqalarida: 3×5=15 (teng, <emas), 3×6=18>15.',
            },
            {
                'savol_matni': 'a + b = 10, a = 3 bo\'lsa, b = ?',
                'variant_a': '13', 'variant_b': '30', 'variant_c': '7', 'variant_d': '3',
                'togri_javob': 'c',
                'izoh': 'b = 10 - a = 10 - 3 = 7.',
            },
            {
                'savol_matni': '(a + b)² ni soddalashtiring (a=2, b=3 uchun hisoblang)',
                'variant_a': '10', 'variant_b': '13', 'variant_c': '25', 'variant_d': '30',
                'togri_javob': 'c',
                'izoh': '(2 + 3)² = 5² = 25.',
            },
            {
                'savol_matni': 'Ali Boboga qaraganda 5 yosh katta, Bob 12 yoshda. Aliga necha yosh?',
                'variant_a': '7', 'variant_b': '17', 'variant_c': '60', 'variant_d': '12',
                'togri_javob': 'b',
                'izoh': 'Ali = Bob + 5 = 12 + 5 = 17 yosh.',
            },
            {
                'savol_matni': '2(3x - 1) = 10. x = ?',
                'variant_a': '1', 'variant_b': '2', 'variant_c': '3', 'variant_d': '4',
                'togri_javob': 'b',
                'izoh': '3x - 1 = 5, 3x = 6, x = 2.',
            },
            {
                'savol_matni': 'n butun son uchun 2n + 1 ifodasi doim qanday son?',
                'variant_a': 'Juft', 'variant_b': 'Toq', 'variant_c': 'Kasr', 'variant_d': 'Manfiy',
                'togri_javob': 'b',
                'izoh': '2n juft son, unga 1 qo\'shilsa, toq son chiqadi.',
            },
            {
                'savol_matni': 'x² = 49. x = ? (musbat qiymat)',
                'variant_a': '6', 'variant_b': '7', 'variant_c': '8', 'variant_d': '9',
                'togri_javob': 'b',
                'izoh': 'x = √49 = 7.',
            },
            {
                'savol_matni': 'Agar 5 qalam 15 000 so\'m tursa, 8 qalam necha so\'m?',
                'variant_a': '20 000', 'variant_b': '24 000', 'variant_c': '18 000', 'variant_d': '40 000',
                'togri_javob': 'b',
                'izoh': '1 qalam = 15 000 ÷ 5 = 3 000 so\'m. 8 qalam = 3 000 × 8 = 24 000 so\'m.',
            },
            {
                'savol_matni': 'x + 2x + 3x = 36. x = ?',
                'variant_a': '4', 'variant_b': '6', 'variant_c': '9', 'variant_d': '12',
                'togri_javob': 'b',
                'izoh': '6x = 36, x = 36 ÷ 6 = 6.',
            },
        ])

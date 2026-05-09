from django.core.management.base import BaseCommand
from apps.models import (
    Kategoriya, Mavzu, Dars, Topshiriq, Savol, Musobaqa, ReytingOyinchi,
    KuchsizSoha, HaftalikFaoliyat, Modul, Yutuq, KunlikSovrin,
    OtaOnaMaslahat, UmumiyStatistika, Profil, OquvSozlama,
    BildirishnomaSozlamasi, Tema, XavfsizlikSozlamasi, DarajaSozlamasi,
    SongiFaoliyat,
)
from datetime import date


class Command(BaseCommand):
    help = "Bazaga boshlang'ich ma'lumotlarni yuklaydi"

    def handle(self, *args, **options):
        self.stdout.write("Ma'lumotlar yuklanmoqda...")

        # Kategoriyalar
        kategoriyalar = {}
        for i, nom in enumerate(['Arifmetika', 'Algebra', 'Geometriya', 'Statistika'], 1):
            obj, _ = Kategoriya.objects.get_or_create(nomi=nom, defaults={'tartib': i})
            kategoriyalar[nom] = obj

        # Mavzular
        mavzu_data = [
            {'raqam': '01', 'nomi': 'Natural sonlar', 'tavsif': 'Sonlar bilan tanishish va ularning xossalari', 'rang': '#e8f5e9', 'icon': '🔢'},
            {'raqam': '02', 'nomi': 'Kasrlar', 'tavsif': "Oddiy va o'nli kasrlar bilan ishlash", 'rang': '#fff3e0', 'icon': '📊'},
            {'raqam': '03', 'nomi': 'Geometriya', 'tavsif': "Shakllar, yuzalar va hajmlarni o'rganish", 'rang': '#e3f2fd', 'icon': '📐'},
            {'raqam': '04', 'nomi': 'Algebra', 'tavsif': "Tenglamalar va tengsizliklarni yechish", 'rang': '#fce4ec', 'icon': '📝'},
        ]
        for i, d in enumerate(mavzu_data):
            Mavzu.objects.get_or_create(raqam=d['raqam'], defaults={**d, 'tartib': i})

        # Darslar (batafsil mazmun bilan)
        dars_data = [
            {
                'raqam': '01', 'nomi': 'Natural sonlar',
                'tavsif': 'Sonlar bilan tanishish va asosiy amallar',
                'icon': '🔢', 'rang': '#e8f5e9', 'davomiylik': '25 daq',
                'holat': 'tugallangan', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>Natural sonlar nima?</h2>
<p>Natural sonlar — bu narsalarni <strong>sanash</strong> uchun ishlatiladigan sonlardir. Ular 1 dan boshlanadi va cheksiz davom etadi:</p>
<div class="formula">1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...</div>

<div class="eslatma">
    <div class="eslatma-title">⚠️ Eslatma</div>
    <p><strong>0 (nol)</strong> natural son emas! Natural sonlar faqat 1 dan boshlanadi.</p>
</div>

<h2>Sonlar qanday yoziladi?</h2>
<p>Biz sonlarni yozish uchun <strong>10 ta raqamdan</strong> foydalanamiz:</p>
<div class="formula">0, 1, 2, 3, 4, 5, 6, 7, 8, 9</div>
<p>Bu raqamlar yordamida ixtiyoriy sonni yozish mumkin.</p>

<h3>Xonalar tizimi</h3>
<p>Har bir raqamning qiymati uning <strong>turgan o'rniga</strong> bog'liq:</p>
<table class="jadval">
    <tr><th>Xona</th><th>Misol (5 274)</th><th>Qiymati</th></tr>
    <tr><td>Birliklar</td><td>4</td><td>4</td></tr>
    <tr><td>O'nliklar</td><td>7</td><td>70</td></tr>
    <tr><td>Yuzliklar</td><td>2</td><td>200</td></tr>
    <tr><td>Mingliklar</td><td>5</td><td>5 000</td></tr>
</table>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p><strong>3 826</strong> sonini tahlil qiling:</p>
    <ul>
        <li>3 — minglar xonasida → 3 000</li>
        <li>8 — yuzlar xonasida → 800</li>
        <li>2 — o'nlar xonasida → 20</li>
        <li>6 — birlar xonasida → 6</li>
    </ul>
    <p>Demak: 3 826 = 3 000 + 800 + 20 + 6</p>
</div>

<h2>Sonlarni taqqoslash</h2>
<p>Ikki natural sonni taqqoslash uchun quyidagi qoidalarga amal qilamiz:</p>
<ol>
    <li>Avval <strong>xonalar sonini</strong> taqqoslang. Xonalari ko'p bo'lgan son kattaroq.</li>
    <li>Xonalar soni teng bo'lsa, <strong>eng yuqori xonadan</strong> boshlab taqqoslang.</li>
</ol>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>Taqqoslang: 489 va 1 203</p>
    <p>489 — 3 xonali, 1 203 — 4 xonali</p>
    <p>Demak: <strong>489 < 1 203</strong></p>
</div>

<h2>Sonlarni yaxlitlash</h2>
<p>Yaxlitlash — sonni eng yaqin "qulay" songa aylantirish.</p>
<ul>
    <li>Agar kesilayotgan raqam <strong>0, 1, 2, 3, 4</strong> bo'lsa — yaxlitlash <strong>pastga</strong> (raqam o'zgarisiz)</li>
    <li>Agar kesilayotgan raqam <strong>5, 6, 7, 8, 9</strong> bo'lsa — yaxlitlash <strong>yuqoriga</strong> (oldingi raqam +1)</li>
</ul>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>3 847 sonini yuzliklargacha yaxlitlang:</p>
    <p>O'nliklar xonasidagi raqam: <strong>4</strong> (< 5) → pastga</p>
    <p>Javob: <strong>3 800</strong></p>
</div>
'''
            },
            {
                'raqam': '02', 'nomi': "Qo'shish va ayirish",
                'tavsif': "Ko'p xonali sonlarni qo'shish va ayirish",
                'icon': '➕', 'rang': '#fff3e0', 'davomiylik': '30 daq',
                'holat': 'tugallangan', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>Qo'shish amali</h2>
<p><strong>Qo'shish</strong> — bu ikki yoki undan ko'p sonni birlashtirish amali. Natijasiga <strong>yig'indi</strong> deyiladi.</p>
<div class="formula">a + b = c<br>qo'shiluvchi + qo'shiluvchi = yig'indi</div>

<h3>Qo'shishning xossalari</h3>
<ul>
    <li><strong>O'rin almashtirish:</strong> a + b = b + a (masalan: 3 + 5 = 5 + 3 = 8)</li>
    <li><strong>Guruhlash:</strong> (a + b) + c = a + (b + c)</li>
    <li><strong>Nolni qo'shish:</strong> a + 0 = a</li>
</ul>

<h3>Ustun bo'yicha qo'shish</h3>
<p>Ko'p xonali sonlarni qo'shishda har bir xonani alohida qo'shamiz:</p>

<div class="misol">
    <div class="misol-title">📝 Misol: 2 567 + 1 845</div>
    <p>Birliklar: 7 + 5 = 12 → 2 yozamiz, 1 ko'chiramiz</p>
    <p>O'nliklar: 6 + 4 + 1 = 11 → 1 yozamiz, 1 ko'chiramiz</p>
    <p>Yuzliklar: 5 + 8 + 1 = 14 → 4 yozamiz, 1 ko'chiramiz</p>
    <p>Mingliklar: 2 + 1 + 1 = 4</p>
    <p><strong>Javob: 4 412</strong></p>
</div>

<h2>Ayirish amali</h2>
<p><strong>Ayirish</strong> — qo'shishning teskari amali. Natijasiga <strong>ayirma</strong> deyiladi.</p>
<div class="formula">a - b = c<br>kamayuvchi - ayiruvchi = ayirma</div>

<h3>Ustun bo'yicha ayirish</h3>
<div class="misol">
    <div class="misol-title">📝 Misol: 5 032 - 1 867</div>
    <p>Birliklar: 2 - 7 → yetmaydi, oldingi xonadan 1 olamiz: 12 - 7 = 5</p>
    <p>O'nliklar: 2 - 6 → yetmaydi (3 emas, chunki 1 berdik): 12 - 6 = 6</p>
    <p>Yuzliklar: 9 - 8 = 1 (10 dan 1 olib berganmiz)</p>
    <p>Mingliklar: 4 - 1 = 3</p>
    <p><strong>Javob: 3 165</strong></p>
</div>

<div class="eslatma">
    <div class="eslatma-title">💡 Tekshirish usuli</div>
    <p>Ayirmani tekshirish uchun javobga ayiruvchini qo'shing. Kamayuvchi chiqishi kerak:</p>
    <p>3 165 + 1 867 = 5 032 ✓</p>
</div>

<h2>Amaliy masalalar</h2>
<div class="misol">
    <div class="misol-title">📝 Masala</div>
    <p>Do'konga ertalab 3 450 ta olma va kechqurun 2 780 ta olma keltirildi. Jami nechta olma keltirildi?</p>
    <p><strong>Yechish:</strong> 3 450 + 2 780 = 6 230 ta olma</p>
</div>
'''
            },
            {
                'raqam': '03', 'nomi': "Ko'paytirish",
                'tavsif': "Ko'paytirish jadvali va usullari",
                'icon': '✖️', 'rang': '#e3f2fd', 'davomiylik': '35 daq',
                'holat': 'tugallangan', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>Ko'paytirish nima?</h2>
<p><strong>Ko'paytirish</strong> — bir sonni boshqa songa necha marta qo'shishni qisqartirish. Natijasiga <strong>ko'paytma</strong> deyiladi.</p>
<div class="formula">a × b = c<br>ko'paytuvchi × ko'paytuvchi = ko'paytma</div>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>4 × 3 = 4 + 4 + 4 = 12</p>
    <p>Ya'ni 4 ni 3 marta qo'shamiz.</p>
</div>

<h2>Ko'paytirish jadvali</h2>
<table class="jadval">
    <tr><th>×</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th></tr>
    <tr><th>2</th><td>2</td><td>4</td><td>6</td><td>8</td><td>10</td><td>12</td><td>14</td><td>16</td><td>18</td></tr>
    <tr><th>3</th><td>3</td><td>6</td><td>9</td><td>12</td><td>15</td><td>18</td><td>21</td><td>24</td><td>27</td></tr>
    <tr><th>4</th><td>4</td><td>8</td><td>12</td><td>16</td><td>20</td><td>24</td><td>28</td><td>32</td><td>36</td></tr>
    <tr><th>5</th><td>5</td><td>10</td><td>15</td><td>20</td><td>25</td><td>30</td><td>35</td><td>40</td><td>45</td></tr>
    <tr><th>6</th><td>6</td><td>12</td><td>18</td><td>24</td><td>30</td><td>36</td><td>42</td><td>48</td><td>54</td></tr>
    <tr><th>7</th><td>7</td><td>14</td><td>21</td><td>28</td><td>35</td><td>42</td><td>49</td><td>56</td><td>63</td></tr>
    <tr><th>8</th><td>8</td><td>16</td><td>24</td><td>32</td><td>40</td><td>48</td><td>56</td><td>64</td><td>72</td></tr>
    <tr><th>9</th><td>9</td><td>18</td><td>27</td><td>36</td><td>45</td><td>54</td><td>63</td><td>72</td><td>81</td></tr>
</table>

<h3>Ko'paytirish xossalari</h3>
<ul>
    <li><strong>O'rin almashtirish:</strong> a × b = b × a</li>
    <li><strong>1 ga ko'paytirish:</strong> a × 1 = a</li>
    <li><strong>0 ga ko'paytirish:</strong> a × 0 = 0</li>
    <li><strong>Taqsimlash:</strong> a × (b + c) = a × b + a × c</li>
</ul>

<h2>Ko'p xonali sonlarni ko'paytirish</h2>
<div class="misol">
    <div class="misol-title">📝 Misol: 243 × 12</div>
    <p><strong>1-qadam:</strong> 243 × 2 = 486</p>
    <p><strong>2-qadam:</strong> 243 × 10 = 2 430</p>
    <p><strong>3-qadam:</strong> 486 + 2 430 = <strong>2 916</strong></p>
</div>

<h2>10, 100, 1000 ga ko'paytirish</h2>
<div class="eslatma">
    <div class="eslatma-title">💡 Tezkor usul</div>
    <p>Sonni 10, 100, 1 000 ga ko'paytirish uchun songa mos ravishda 1, 2, 3 ta <strong>nol qo'shing</strong>:</p>
    <ul>
        <li>45 × 10 = 450</li>
        <li>45 × 100 = 4 500</li>
        <li>45 × 1 000 = 45 000</li>
    </ul>
</div>
'''
            },
            {
                'raqam': '04', 'nomi': "Bo'lish",
                'tavsif': "Sonlarni bo'lish va qoldiqli bo'lish",
                'icon': '➗', 'rang': '#fce4ec', 'davomiylik': '30 daq',
                'holat': 'jarayonda', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>Bo'lish nima?</h2>
<p><strong>Bo'lish</strong> — ko'paytirishning teskari amali. U bir sonni teng qismlarga ajratishdir.</p>
<div class="formula">a ÷ b = c<br>bo'linuvchi ÷ bo'luvchi = bo'linma</div>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>12 ÷ 3 = 4, chunki 3 × 4 = 12</p>
    <p>Ya'ni 12 ni 3 teng qismga bo'lsak, har bir qismda 4 bo'ladi.</p>
</div>

<h2>Qoldiqli bo'lish</h2>
<p>Har doim ham son teng bo'linmaydi. Bunday hollarda <strong>qoldiq</strong> paydo bo'ladi.</p>
<div class="formula">a = b × c + d<br>bo'linuvchi = bo'luvchi × bo'linma + qoldiq</div>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>17 ÷ 5 = 3 (qoldiq 2)</p>
    <p>Tekshirish: 5 × 3 + 2 = 17 ✓</p>
</div>

<div class="eslatma">
    <div class="eslatma-title">⚠️ Muhim qoida</div>
    <p><strong>Qoldiq har doim bo'luvchidan kichik bo'lishi kerak!</strong></p>
    <p>Masalan, 5 ga bo'lganda qoldiq 0, 1, 2, 3 yoki 4 bo'lishi mumkin.</p>
</div>

<h2>Ustunli bo'lish</h2>
<div class="misol">
    <div class="misol-title">📝 Misol: 756 ÷ 6</div>
    <p><strong>1-qadam:</strong> 7 ÷ 6 = 1 (qoldiq 1)</p>
    <p><strong>2-qadam:</strong> 15 ÷ 6 = 2 (qoldiq 3)</p>
    <p><strong>3-qadam:</strong> 36 ÷ 6 = 6 (qoldiq 0)</p>
    <p><strong>Javob: 126</strong></p>
</div>

<h2>Bo'lish belgilari</h2>
<ul>
    <li>Agar son <strong>2 ga</strong> bo'linsa — u juft son (oxirgi raqami: 0, 2, 4, 6, 8)</li>
    <li>Agar son <strong>5 ga</strong> bo'linsa — oxirgi raqami 0 yoki 5</li>
    <li>Agar son <strong>10 ga</strong> bo'linsa — oxirgi raqami 0</li>
    <li>Agar son <strong>3 ga</strong> bo'linsa — raqamlari yig'indisi 3 ga bo'linadi</li>
    <li>Agar son <strong>9 ga</strong> bo'linsa — raqamlari yig'indisi 9 ga bo'linadi</li>
</ul>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>528 soni 3 ga bo'linadimi?</p>
    <p>Raqamlar yig'indisi: 5 + 2 + 8 = 15</p>
    <p>15 ÷ 3 = 5 → <strong>Ha, bo'linadi!</strong></p>
</div>
'''
            },
            {
                'raqam': '05', 'nomi': 'Kasrlar',
                'tavsif': 'Oddiy kasrlar va ular ustida amallar',
                'icon': '📊', 'rang': '#f3e5f5', 'davomiylik': '40 daq',
                'holat': 'jarayonda', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>Kasr nima?</h2>
<p><strong>Kasr</strong> — butun sonning bir qismini ifodalash usuli. Kasr ikki qismdan iborat:</p>
<div class="formula">a/b<br>surat / maxraj</div>
<ul>
    <li><strong>Surat (a)</strong> — olingan qismlar soni</li>
    <li><strong>Maxraj (b)</strong> — umumiy qismlar soni</li>
</ul>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>Pitsa 8 ga bo'lingan, 3 tasini yedingiz. Necha qismi qoldi?</p>
    <p>Yegan qismingiz: <strong>3/8</strong></p>
    <p>Qolgan qismi: <strong>5/8</strong></p>
</div>

<h2>Kasrlarni qo'shish va ayirish</h2>
<h3>Maxrajlari teng bo'lsa:</h3>
<div class="formula">a/c + b/c = (a + b)/c</div>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>2/7 + 3/7 = (2 + 3)/7 = <strong>5/7</strong></p>
</div>

<h3>Maxrajlari farq bo'lsa:</h3>
<p>Avval umumiy maxraj topiladi:</p>
<div class="misol">
    <div class="misol-title">📝 Misol: 1/3 + 1/4</div>
    <p>Umumiy maxraj: 12 (3 va 4 ning eng kichik umumiy karrali)</p>
    <p>1/3 = 4/12</p>
    <p>1/4 = 3/12</p>
    <p>4/12 + 3/12 = <strong>7/12</strong></p>
</div>

<h2>Kasrlarni ko'paytirish</h2>
<div class="formula">a/b × c/d = (a × c) / (b × d)</div>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>2/3 × 4/5 = (2 × 4) / (3 × 5) = <strong>8/15</strong></p>
</div>

<h2>Kasrlarni bo'lish</h2>
<div class="formula">a/b ÷ c/d = a/b × d/c</div>
<p>Bo'lishda ikkinchi kasrni <strong>teskari</strong> qilib ko'paytiramiz.</p>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>3/4 ÷ 2/5 = 3/4 × 5/2 = 15/8 = <strong>1 7/8</strong></p>
</div>

<h2>Kasrni qisqartirish</h2>
<p>Surat va maxrajni ularning <strong>EKUB (eng katta umumiy bo'luvchi)</strong> ga bo'lamiz:</p>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>12/18 → EKUB(12, 18) = 6</p>
    <p>12/18 = (12÷6)/(18÷6) = <strong>2/3</strong></p>
</div>
'''
            },
            {
                'raqam': '06', 'nomi': "O'nli kasrlar",
                'tavsif': "O'nli kasrlar bilan ishlash",
                'icon': '🔣', 'rang': '#e0f7fa', 'davomiylik': '35 daq',
                'holat': 'qulflangan', 'kat': 'Arifmetika',
                'mazmun': '''
<h2>O'nli kasr nima?</h2>
<p><strong>O'nli kasr</strong> — maxraji 10, 100, 1000, ... bo'lgan kasrni vergul bilan yozish usuli.</p>
<div class="formula">3/10 = 0,3 &nbsp;&nbsp; 25/100 = 0,25 &nbsp;&nbsp; 7/1000 = 0,007</div>

<h3>O'nli kasrning xonalari</h3>
<table class="jadval">
    <tr><th>Son</th><th>Birlik</th><th>,</th><th>O'ndan bir</th><th>Yuzdan bir</th><th>Mingdan bir</th></tr>
    <tr><td>3,547</td><td>3</td><td>,</td><td>5</td><td>4</td><td>7</td></tr>
</table>

<h2>O'nli kasrlarni qo'shish va ayirish</h2>
<p>Vergulni vergul ostiga qo'yib, oddiy qo'shish/ayirish bajaramiz:</p>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>3,25 + 1,7 = ?</p>
    <p>3,25 + 1,70 = <strong>4,95</strong></p>
</div>

<h2>O'nli kasrlarni ko'paytirish</h2>
<p>Avval vergulsiz ko'paytiramiz, keyin verguldan keyingi raqamlar sonini hisoblaymiz:</p>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>2,3 × 1,5 = ?</p>
    <p>23 × 15 = 345</p>
    <p>Verguldan keyin jami 2 ta raqam → <strong>3,45</strong></p>
</div>

<h2>O'nli kasrdan oddiy kasrga o'tish</h2>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>0,75 = 75/100 = <strong>3/4</strong></p>
    <p>0,6 = 6/10 = <strong>3/5</strong></p>
</div>
'''
            },
            {
                'raqam': '07', 'nomi': 'Foizlar',
                'tavsif': "Foizlarni hisoblash va qo'llash",
                'icon': '💯', 'rang': '#fff9c4', 'davomiylik': '30 daq',
                'holat': 'qulflangan', 'kat': 'Algebra',
                'mazmun': '''
<h2>Foiz nima?</h2>
<p><strong>Foiz</strong> — bu yuzdan bir qism. 1% = 1/100 = 0,01</p>
<div class="formula">1% = 1/100 = 0,01<br>50% = 50/100 = 1/2<br>100% = butun son</div>

<h2>Sonning foizini topish</h2>
<div class="formula">Sonning a% = Son × a / 100</div>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>200 ning 15% ini toping:</p>
    <p>200 × 15 / 100 = <strong>30</strong></p>
</div>

<h2>Foizni topish</h2>
<div class="formula">Foiz = (qism / butun) × 100%</div>
<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>Sinfda 30 o'quvchi bor, 12 tasi qiz. Qizlar necha foiz?</p>
    <p>(12 / 30) × 100% = <strong>40%</strong></p>
</div>

<h2>Amaliy masalalar</h2>
<div class="misol">
    <div class="misol-title">📝 Chegirma masalasi</div>
    <p>Ko'ylak narxi 80 000 so'm. 25% chegirma bilan qancha bo'ladi?</p>
    <p>Chegirma: 80 000 × 25 / 100 = 20 000 so'm</p>
    <p>Yangi narx: 80 000 - 20 000 = <strong>60 000 so'm</strong></p>
</div>
'''
            },
            {
                'raqam': '08', 'nomi': 'Geometrik shakllar',
                'tavsif': 'Asosiy geometrik shakllar va xossalari',
                'icon': '📐', 'rang': '#e8eaf6', 'davomiylik': '35 daq',
                'holat': 'qulflangan', 'kat': 'Geometriya',
                'mazmun': '''
<h2>Asosiy geometrik shakllar</h2>

<h3>1. Uchburchak</h3>
<p>Uchburchak — 3 ta tomon va 3 ta burchakdan iborat shakl.</p>
<ul>
    <li><strong>Teng tomonli</strong> — barcha tomonlari teng</li>
    <li><strong>Teng yonli</strong> — 2 ta tomoni teng</li>
    <li><strong>To'g'ri burchakli</strong> — bitta burchagi 90°</li>
</ul>
<div class="formula">Burchaklar yig'indisi = 180°</div>

<h3>2. To'rtburchak</h3>
<p><strong>To'g'ri to'rtburchak</strong> — barcha burchaklari 90°</p>
<p><strong>Kvadrat</strong> — barcha tomonlari va burchaklari teng</p>

<h3>3. Doira</h3>
<p>Doira — markazdan teng masofada joylashgan nuqtalar to'plami.</p>
<ul>
    <li><strong>Radius (r)</strong> — markazdan chekkagacha masofa</li>
    <li><strong>Diametr (d)</strong> — d = 2r</li>
</ul>

<h2>Burchaklar</h2>
<table class="jadval">
    <tr><th>Burchak turi</th><th>O'lchami</th></tr>
    <tr><td>O'tkir burchak</td><td>0° dan 90° gacha</td></tr>
    <tr><td>To'g'ri burchak</td><td>90°</td></tr>
    <tr><td>O'tmas burchak</td><td>90° dan 180° gacha</td></tr>
    <tr><td>Yoyiq burchak</td><td>180°</td></tr>
</table>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>Uchburchakning 2 ta burchagi 60° va 80°. Uchinchi burchakni toping.</p>
    <p>180° - 60° - 80° = <strong>40°</strong></p>
</div>
'''
            },
            {
                'raqam': '09', 'nomi': 'Perimetr va yuza',
                'tavsif': 'Shakllarning perimetri va yuzasini hisoblash',
                'icon': '📏', 'rang': '#efebe9', 'davomiylik': '40 daq',
                'holat': 'qulflangan', 'kat': 'Geometriya',
                'mazmun': '''
<h2>Perimetr</h2>
<p><strong>Perimetr</strong> — shaklning barcha tomonlari yig'indisi.</p>

<table class="jadval">
    <tr><th>Shakl</th><th>Formulasi</th></tr>
    <tr><td>Kvadrat</td><td>P = 4a</td></tr>
    <tr><td>To'g'ri to'rtburchak</td><td>P = 2(a + b)</td></tr>
    <tr><td>Uchburchak</td><td>P = a + b + c</td></tr>
    <tr><td>Doira (aylana)</td><td>C = 2πr ≈ 6,28r</td></tr>
</table>

<div class="misol">
    <div class="misol-title">📝 Misol</div>
    <p>To'g'ri to'rtburchak tomonlari: a = 8 sm, b = 5 sm</p>
    <p>P = 2 × (8 + 5) = 2 × 13 = <strong>26 sm</strong></p>
</div>

<h2>Yuza</h2>
<p><strong>Yuza</strong> — shaklning ichki qismining o'lchami (kvadrat birlikda).</p>

<table class="jadval">
    <tr><th>Shakl</th><th>Formulasi</th></tr>
    <tr><td>Kvadrat</td><td>S = a²</td></tr>
    <tr><td>To'g'ri to'rtburchak</td><td>S = a × b</td></tr>
    <tr><td>Uchburchak</td><td>S = (a × h) / 2</td></tr>
    <tr><td>Doira</td><td>S = πr² ≈ 3,14 × r²</td></tr>
</table>

<div class="misol">
    <div class="misol-title">📝 Misol 1</div>
    <p>Kvadratning tomoni 6 sm. Yuzasini toping.</p>
    <p>S = 6² = <strong>36 sm²</strong></p>
</div>

<div class="misol">
    <div class="misol-title">📝 Misol 2</div>
    <p>Uchburchak asosi 10 sm, balandligi 8 sm. Yuzasini toping.</p>
    <p>S = (10 × 8) / 2 = <strong>40 sm²</strong></p>
</div>

<div class="misol">
    <div class="misol-title">📝 Misol 3 — Amaliy masala</div>
    <p>Xona o'lchamlari 5m × 4m. Polga plitka yotqizish uchun necha m² plitka kerak?</p>
    <p>S = 5 × 4 = <strong>20 m²</strong></p>
</div>

<div class="eslatma">
    <div class="eslatma-title">💡 Eslatma</div>
    <p>Yuza o'lchov birliklari: mm², sm², dm², m², km²</p>
    <p>1 m² = 10 000 sm²</p>
</div>
'''
            },
        ]
        for i, d in enumerate(dars_data):
            kat = kategoriyalar.get(d.pop('kat'))
            mazmun = d.pop('mazmun', '')
            obj, created = Dars.objects.get_or_create(
                raqam=d['raqam'],
                defaults={**d, 'kategoriya': kat, 'tartib': i, 'mazmun': mazmun}
            )
            if not created and not obj.mazmun:
                obj.mazmun = mazmun
                obj.save()

        # Topshiriqlar
        topshiriq_data = [
            {'nomi': "10 ta qo'shish misoli", 'icon': '➕', 'rang': '#e8f5e9', 'savollar': 10, 'foiz': 60, 'progress_rang': '#4caf50', 'btn_rang': '#4caf50', 'turi': 'kichik'},
            {'nomi': 'Ayirish mashqlari', 'icon': '➖', 'rang': '#e3f2fd', 'savollar': 10, 'foiz': 30, 'progress_rang': '#2196f3', 'btn_rang': '#2196f3', 'turi': 'kichik'},
            {'nomi': "Ko'paytirish jadvali", 'icon': '✖️', 'rang': '#fff3e0', 'savollar': 10, 'foiz': 0, 'progress_rang': '#ff9800', 'btn_rang': '#ff9800', 'turi': 'kichik'},
            {'nomi': "Bo'lish mashqlari", 'icon': '➗', 'rang': '#fce4ec', 'savollar': 10, 'foiz': 0, 'progress_rang': '#e91e63', 'btn_rang': '#e91e63', 'turi': 'kichik'},
            {'nomi': 'Geometrik shakllarni tani', 'tavsif': 'Geometrik shakllarni aniqlash va nomlarini bilish', 'rang': '#e8eaf6', 'savollar': 8, 'foiz': 0, 'progress_rang': '#5c6bc0', 'btn_rang': '#5c6bc0', 'rasm_url': 'https://images.unsplash.com/photo-1635372722656-389f87a941b7?w=180&h=140&fit=crop', 'turi': 'pastki'},
            {'nomi': 'Kasrlar sinovi', 'tavsif': 'Oddiy kasrlar ustida amallar bajarish', 'rang': '#f3e5f5', 'savollar': 8, 'foiz': 0, 'progress_rang': '#9c27b0', 'btn_rang': '#9c27b0', 'rasm_url': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=180&h=140&fit=crop', 'turi': 'pastki'},
        ]
        for i, d in enumerate(topshiriq_data):
            Topshiriq.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # SAVOLLAR
        self._savollar_yuklash()

        # Musobaqalar
        musobaqa_data = [
            {'nomi': 'Sonlar Marafoni', 'tavsif': 'Tezlik bilan misollarni yeching va raqiblarga qarshi bellashing', 'icon': '🏃', 'rang': '#e8f5e9', 'qatnashchilar': 128, 'daraja': "O'rta"},
            {'nomi': "Mantiqiy o'yinlar", 'tavsif': 'Mantiqiy masalalarni yechib, fikrlash qobiliyatingizni sinang', 'icon': '🧩', 'rang': '#e3f2fd', 'qatnashchilar': 86, 'daraja': 'Qiyin'},
            {'nomi': 'Geometriya chempionati', 'tavsif': "Shakllar va formulalar bo'yicha bilimingizni ko'rsating", 'icon': '📐', 'rang': '#fff3e0', 'qatnashchilar': 64, 'daraja': 'Oson'},
            {'nomi': 'Algebra turniri', 'tavsif': "Tenglamalar va ifodalar bo'yicha raqobatlashing", 'icon': '📝', 'rang': '#fce4ec', 'qatnashchilar': 95, 'daraja': "O'rta"},
        ]
        for i, d in enumerate(musobaqa_data):
            Musobaqa.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Reyting
        reyting_data = [
            {'ism': 'Aziza K.', 'ball': 2450, 'medal': '🥇'},
            {'ism': 'Jasur M.', 'ball': 2380, 'medal': '🥈'},
            {'ism': 'Nilufar T.', 'ball': 2290, 'medal': '🥉'},
            {'ism': 'Sardor A.', 'ball': 2150, 'medal': ''},
            {'ism': 'Madina R.', 'ball': 2080, 'medal': ''},
        ]
        for i, d in enumerate(reyting_data):
            ReytingOyinchi.objects.get_or_create(ism=d['ism'], defaults={**d, 'tartib': i})

        # Kuchsiz sohalar
        kuchsiz_data = [
            {'nomi': "Ko'paytirish jadvali", 'foiz': 45, 'rang': '#ff7043'},
            {'nomi': "Kasrlarni qo'shish", 'foiz': 60, 'rang': '#ffa726'},
            {'nomi': 'Geometrik shakllar', 'foiz': 70, 'rang': '#66bb6a'},
        ]
        for i, d in enumerate(kuchsiz_data):
            KuchsizSoha.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Haftalik faoliyat
        haftalik_data = [
            {'kun': 'Du', 'soat': 2.5, 'foiz': 50},
            {'kun': 'Se', 'soat': 4.0, 'foiz': 80},
            {'kun': 'Cho', 'soat': 1.5, 'foiz': 30},
            {'kun': 'Pa', 'soat': 3.5, 'foiz': 70},
            {'kun': 'Ju', 'soat': 5.0, 'foiz': 100},
            {'kun': 'Sha', 'soat': 2.0, 'foiz': 40},
            {'kun': 'Ya', 'soat': 3.0, 'foiz': 60},
        ]
        for i, d in enumerate(haftalik_data):
            HaftalikFaoliyat.objects.get_or_create(kun=d['kun'], defaults={**d, 'tartib': i})

        # Modullar
        modul_data = [
            {'nomi': 'Arifmetika', 'icon': '🔢', 'rang': '#e8f5e9', 'ball': 92, 'holat': "A'lo", 'progress_rang': '#4caf50'},
            {'nomi': 'Geometriya', 'icon': '📐', 'rang': '#e3f2fd', 'ball': 78, 'holat': 'Yaxshi', 'progress_rang': '#2196f3'},
            {'nomi': 'Algebra', 'icon': '📝', 'rang': '#fff3e0', 'ball': 65, 'holat': "O'rta", 'progress_rang': '#ff9800'},
            {'nomi': 'Statistika', 'icon': '📊', 'rang': '#fce4ec', 'ball': 85, 'holat': 'Yaxshi', 'progress_rang': '#e91e63'},
            {'nomi': 'Mantiq', 'icon': '🧩', 'rang': '#f3e5f5', 'ball': 70, 'holat': "O'rta", 'progress_rang': '#9c27b0'},
            {'nomi': 'Kasrlar', 'icon': '🔣', 'rang': '#e0f7fa', 'ball': 88, 'holat': 'Yaxshi', 'progress_rang': '#00bcd4'},
        ]
        for i, d in enumerate(modul_data):
            Modul.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Yutuqlar
        yutuq_data = [
            {'nomi': 'Birinchi qadam', 'icon': '🏅', 'rang': '#fff3e0', 'tavsif': '10 ta topshiriq bajardingiz', 'ball': 50, 'sana': date(2024, 1, 15), 'olingan': True},
            {'nomi': 'Tez hisoblash', 'icon': '⚡', 'rang': '#e3f2fd', 'tavsif': '1 daqiqada 20 ta misol yechdingiz', 'ball': 100, 'sana': date(2024, 1, 20), 'olingan': True},
            {'nomi': 'Geometr', 'icon': '📐', 'rang': '#e8f5e9', 'tavsif': "Geometriya bo'limini tugatdingiz", 'ball': 150, 'sana': date(2024, 2, 5), 'olingan': True, 'progress_rang': '#4caf50'},
            {'nomi': 'Izchil', 'icon': '🔥', 'rang': '#fce4ec', 'tavsif': '7 kun ketma-ket mashq qildingiz', 'ball': 200, 'sana': date(2024, 2, 10), 'olingan': True, 'progress_rang': '#e91e63'},
            {'nomi': 'Bilimdon', 'icon': '🎓', 'rang': '#f3e5f5', 'tavsif': "5 ta darsni a'lo bahoga tugatdingiz", 'ball': 120, 'sana': date(2024, 2, 18), 'olingan': True, 'progress_rang': '#9c27b0'},
            {'nomi': 'Arifmetik', 'icon': '🔢', 'rang': '#e0f7fa', 'tavsif': "Arifmetika bo'limini tugatdingiz", 'ball': 150, 'sana': date(2024, 3, 1), 'olingan': True, 'progress_rang': '#00bcd4'},
            {'nomi': 'Matematika ustasi', 'icon': '👑', 'rang': '#fff9e6', 'tavsif': "Barcha bo'limlarni tugatish", 'ball': 500, 'olingan': False, 'foiz': 60, 'progress_rang': '#f5c542'},
            {'nomi': 'Chempion', 'icon': '🏆', 'rang': '#f0f0f0', 'tavsif': "3 ta musobaqada g'olib bo'lish", 'ball': 300, 'olingan': False, 'foiz': 33, 'progress_rang': '#9e9e9e'},
            {'nomi': '30 kunlik marafon', 'icon': '📅', 'rang': '#fce4ec', 'tavsif': '30 kun ketma-ket mashq qilish', 'ball': 400, 'olingan': False, 'foiz': 23, 'progress_rang': '#e91e63'},
            {'nomi': 'Tezkor', 'icon': '🚀', 'rang': '#e3f2fd', 'tavsif': '1 daqiqada 50 ta misol yechish', 'ball': 250, 'olingan': False, 'foiz': 40, 'progress_rang': '#2196f3'},
        ]
        for i, d in enumerate(yutuq_data):
            Yutuq.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Kunlik sovrinlar
        kunlik_data = [
            {'kun': 'Du', 'icon': '⭐', 'ball': 10, 'olingan': True},
            {'kun': 'Se', 'icon': '⭐', 'ball': 10, 'olingan': True},
            {'kun': 'Cho', 'icon': '⭐', 'ball': 10, 'olingan': True},
            {'kun': 'Pa', 'icon': '⭐', 'ball': 10, 'olingan': True},
            {'kun': 'Ju', 'icon': '🎁', 'ball': 25, 'olingan': False},
            {'kun': 'Sha', 'icon': '⭐', 'ball': 10, 'olingan': False},
            {'kun': 'Ya', 'icon': '🎁', 'ball': 50, 'olingan': False},
        ]
        for i, d in enumerate(kunlik_data):
            KunlikSovrin.objects.get_or_create(kun=d['kun'], defaults={**d, 'tartib': i})

        # Ota-ona maslahatlari
        maslahat_data = [
            {'nomi': 'Kuchli tomonlari', 'icon': '💪', 'rang': '#e8f5e9', 'tavsif': "Arifmetika va kasrlar bo'yicha a'lo natijalar ko'rsatmoqda"},
            {'nomi': 'Yaxshilash kerak', 'icon': '📈', 'rang': '#fff3e0', 'tavsif': "Algebra va mantiq bo'yicha qo'shimcha mashqlar tavsiya etiladi"},
            {'nomi': 'Tavsiyalar', 'icon': '💡', 'rang': '#e3f2fd', 'tavsif': 'Har kuni 30 daqiqa mashq qilish natijalarni sezilarli yaxshilaydi'},
        ]
        for i, d in enumerate(maslahat_data):
            OtaOnaMaslahat.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Umumiy statistika
        UmumiyStatistika.objects.get_or_create(pk=1, defaults={
            'umumiy_ball': 82, 'bajarilgan': 24, 'jarayonda': 12,
            'umumiy_soat': 47, 'ketma_ket_kun': 7, 'ortacha_ball_foiz': 89,
            'yulduzcha': 150,
        })

        # Profil
        Profil.objects.get_or_create(pk=1, defaults={
            'ism': 'Ali', 'familiya': 'Valiyev', 'email': 'ali.valiyev@email.com',
            'yosh': 12, 'sinf': '6-sinf', 'maktab': "15-son umumta'lim maktabi",
        })

        # O'quv sozlamalari
        oquv_data = [
            {'nomi': 'Qiyinlik darajasi', 'tavsif': 'Topshiriqlar qiyinlik darajasini tanlang', 'icon': 'sliders-h', 'rang': '#e8f5e9', 'icon_rang': '#4caf50', 'turi': 'select', 'qiymat_text': "O'rta"},
            {'nomi': 'Avtomatik tekshirish', 'tavsif': 'Javoblarni darhol tekshirish', 'icon': 'check-double', 'rang': '#e3f2fd', 'icon_rang': '#2196f3', 'turi': 'toggle', 'qiymat_bool': True},
            {'nomi': 'Vaqt chegarasi', 'tavsif': 'Har bir topshiriq uchun vaqt chegarasi', 'icon': 'stopwatch', 'rang': '#fff3e0', 'icon_rang': '#ff9800', 'turi': 'toggle', 'qiymat_bool': False},
            {'nomi': 'Maslahatlar', 'tavsif': "Topshiriq yechish vaqtida maslahatlar ko'rsatish", 'icon': 'lightbulb', 'rang': '#f3e5f5', 'icon_rang': '#9c27b0', 'turi': 'toggle', 'qiymat_bool': True},
            {'nomi': 'Kunlik maqsad', 'tavsif': "Kunlik yechilishi kerak bo'lgan topshiriqlar soni", 'icon': 'bullseye', 'rang': '#fce4ec', 'icon_rang': '#e91e63', 'turi': 'select', 'qiymat_text': '10 ta'},
        ]
        for i, d in enumerate(oquv_data):
            OquvSozlama.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Bildirishnoma sozlamalari
        bildirishnoma_data = [
            {'nomi': 'Eslatmalar', 'tavsif': 'Kunlik mashq qilish eslatmalari', 'icon': 'bell', 'rang': '#fff3e0', 'icon_rang': '#f0a500', 'yoqilgan': True},
            {'nomi': 'Yutuq xabarlari', 'tavsif': 'Yangi yutuq olganingizda xabar berish', 'icon': 'trophy', 'rang': '#e8f5e9', 'icon_rang': '#4caf50', 'yoqilgan': True},
            {'nomi': 'Haftalik hisobot', 'tavsif': 'Har hafta natijalar haqida xabar', 'icon': 'chart-bar', 'rang': '#e3f2fd', 'icon_rang': '#2196f3', 'yoqilgan': False},
            {'nomi': 'Musobaqa xabarlari', 'tavsif': 'Yangi musobaqalar haqida xabar berish', 'icon': 'flag-checkered', 'rang': '#fce4ec', 'icon_rang': '#e91e63', 'yoqilgan': True},
        ]
        for i, d in enumerate(bildirishnoma_data):
            BildirishnomaSozlamasi.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Temalar
        tema_data = [
            {'nomi': "Yorug'", 'rang': '#fff', 'preview_rang': '#f5f0eb', 'tanlangan': True},
            {'nomi': "Qorong'i", 'rang': '#2d2d3f', 'preview_rang': '#1a1a2e', 'tanlangan': False},
            {'nomi': "Ko'k", 'rang': '#e3f2fd', 'preview_rang': '#bbdefb', 'tanlangan': False},
            {'nomi': 'Yashil', 'rang': '#e8f5e9', 'preview_rang': '#c8e6c9', 'tanlangan': False},
        ]
        for i, d in enumerate(tema_data):
            Tema.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # Xavfsizlik sozlamalari
        xavfsizlik_data = [
            {'nomi': "Parolni o'zgartirish", 'tavsif': 'Hisob parolini yangilash', 'icon': 'lock', 'rang': '#fff3e0', 'icon_rang': '#f0a500'},
            {'nomi': 'Ikki bosqichli tasdiqlash', 'tavsif': "Qo'shimcha xavfsizlik qatlami", 'icon': 'shield-alt', 'rang': '#e8f5e9', 'icon_rang': '#4caf50'},
            {'nomi': 'Faol seanslar', 'tavsif': 'Barcha faol qurilmalarni boshqarish', 'icon': 'desktop', 'rang': '#e3f2fd', 'icon_rang': '#2196f3'},
        ]
        for i, d in enumerate(xavfsizlik_data):
            XavfsizlikSozlamasi.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        # So'nggi faoliyatlar
        faoliyat_data = [
            {'nomi': 'Natural sonlar - 95%', 'rang': '#4caf50', 'sahifa': 'bosh_sahifa'},
            {'nomi': 'Kasrlar - 78%', 'rang': '#ff9800', 'sahifa': 'bosh_sahifa'},
            {'nomi': 'Geometriya - 82%', 'rang': '#2196f3', 'sahifa': 'bosh_sahifa'},
            {"nomi": "Qo'shish - 95% to'g'ri", 'rang': '#4caf50', 'sahifa': 'topshiriqlar'},
            {'nomi': 'Ayirish - jarayonda', 'rang': '#ff9800', 'sahifa': 'topshiriqlar'},
            {"nomi": "Ko'paytirish - boshlanmagan", 'rang': '#ccc', 'sahifa': 'topshiriqlar'},
            {'nomi': 'Hisob faol', 'rang': '#4caf50', 'sahifa': 'sozlamalar'},
            {'nomi': 'Premium rejasi', 'rang': '#2196f3', 'sahifa': 'sozlamalar'},
            {"nomi": "2024-dan beri a'zo", 'rang': '#ff9800', 'sahifa': 'sozlamalar'},
        ]
        for i, d in enumerate(faoliyat_data):
            SongiFaoliyat.objects.get_or_create(nomi=d['nomi'], sahifa=d['sahifa'], defaults={**d, 'tartib': i})

        # Darajalar
        daraja_data = [
            {'nomi': "Bronza", 'icon': '🥉', 'kerakli_ball': 200},
            {'nomi': "Kumush", 'icon': '🥈', 'kerakli_ball': 500},
            {'nomi': "Oltin", 'icon': '🥇', 'kerakli_ball': 1000},
            {'nomi': "Brilliant", 'icon': '💎', 'kerakli_ball': 2000},
        ]
        for i, d in enumerate(daraja_data):
            DarajaSozlamasi.objects.get_or_create(nomi=d['nomi'], defaults={**d, 'tartib': i})

        self.stdout.write(self.style.SUCCESS("Barcha ma'lumotlar muvaffaqiyatli yuklandi!"))

    def _savollar_yuklash(self):
        """Har bir topshiriq uchun savollar"""

        # 1. Qo'shish misollari
        top = Topshiriq.objects.filter(nomi__icontains="qo'shish").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': '25 + 17 = ?', 'variant_a': '41', 'variant_b': '42', 'variant_c': '43', 'variant_d': '44', 'togri_javob': 'b', 'izoh': '25 + 17: birliklar 5+7=12, 2 yozamiz 1 ko\'chiramiz. O\'nliklar 2+1+1=4. Javob: 42'},
                {'savol_matni': '156 + 244 = ?', 'variant_a': '390', 'variant_b': '400', 'variant_c': '410', 'variant_d': '300', 'togri_javob': 'b', 'izoh': '156 + 244 = 400'},
                {'savol_matni': '999 + 1 = ?', 'variant_a': '1 000', 'variant_b': '999', 'variant_c': '1 001', 'variant_d': '990', 'togri_javob': 'a', 'izoh': '999 + 1 = 1 000. 9+1=10, har xonadan ko\'chiriladi.'},
                {'savol_matni': '48 + 52 = ?', 'variant_a': '90', 'variant_b': '110', 'variant_c': '100', 'variant_d': '98', 'togri_javob': 'c', 'izoh': '48 + 52 = 100'},
                {'savol_matni': '1 234 + 766 = ?', 'variant_a': '1 900', 'variant_b': '2 000', 'variant_c': '1 990', 'variant_d': '2 100', 'togri_javob': 'b', 'izoh': '1 234 + 766 = 2 000'},
                {'savol_matni': '375 + 425 = ?', 'variant_a': '700', 'variant_b': '800', 'variant_c': '750', 'variant_d': '900', 'togri_javob': 'b', 'izoh': '375 + 425 = 800'},
                {'savol_matni': '89 + 11 = ?', 'variant_a': '99', 'variant_b': '100', 'variant_c': '101', 'variant_d': '90', 'togri_javob': 'b', 'izoh': '89 + 11 = 100'},
                {'savol_matni': '2 500 + 3 500 = ?', 'variant_a': '5 000', 'variant_b': '6 000', 'variant_c': '5 500', 'variant_d': '7 000', 'togri_javob': 'b', 'izoh': 'Mingliklarni qo\'shamiz: 2+3=5, yuzliklarni: 5+5=10. Javob: 6 000'},
                {'savol_matni': '67 + 33 + 50 = ?', 'variant_a': '140', 'variant_b': '150', 'variant_c': '160', 'variant_d': '145', 'togri_javob': 'b', 'izoh': '67 + 33 = 100, keyin 100 + 50 = 150'},
                {'savol_matni': 'Do\'konga 450 ta olma va 350 ta nok keltirildi. Jami nechta meva bor?', 'variant_a': '700', 'variant_b': '800', 'variant_c': '900', 'variant_d': '750', 'togri_javob': 'b', 'izoh': '450 + 350 = 800 ta meva'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

        # 2. Ayirish mashqlari
        top = Topshiriq.objects.filter(nomi__icontains="Ayirish").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': '50 - 23 = ?', 'variant_a': '27', 'variant_b': '33', 'variant_c': '37', 'variant_d': '23', 'togri_javob': 'a', 'izoh': '50 - 23 = 27'},
                {'savol_matni': '100 - 47 = ?', 'variant_a': '63', 'variant_b': '53', 'variant_c': '57', 'variant_d': '43', 'togri_javob': 'b', 'izoh': '100 - 47 = 53'},
                {'savol_matni': '1 000 - 365 = ?', 'variant_a': '635', 'variant_b': '645', 'variant_c': '735', 'variant_d': '535', 'togri_javob': 'a', 'izoh': '1 000 - 365 = 635'},
                {'savol_matni': '500 - 199 = ?', 'variant_a': '301', 'variant_b': '311', 'variant_c': '299', 'variant_d': '201', 'togri_javob': 'a', 'izoh': '500 - 199 = 301. Tezkor usul: 500 - 200 + 1 = 301'},
                {'savol_matni': '842 - 356 = ?', 'variant_a': '486', 'variant_b': '496', 'variant_c': '586', 'variant_d': '476', 'togri_javob': 'a', 'izoh': '842 - 356: birliklar 12-6=6, o\'nliklar 3-5 (yetmaydi, 13-5=8, yuzlik -1), yuzliklar 7-3=4. Javob: 486'},
                {'savol_matni': '2 000 - 1 250 = ?', 'variant_a': '850', 'variant_b': '750', 'variant_c': '650', 'variant_d': '550', 'togri_javob': 'b', 'izoh': '2 000 - 1 250 = 750'},
                {'savol_matni': '75 - 28 = ?', 'variant_a': '47', 'variant_b': '57', 'variant_c': '43', 'variant_d': '53', 'togri_javob': 'a', 'izoh': '75 - 28 = 47'},
                {'savol_matni': '310 - 175 = ?', 'variant_a': '145', 'variant_b': '135', 'variant_c': '125', 'variant_d': '155', 'togri_javob': 'b', 'izoh': '310 - 175 = 135'},
                {'savol_matni': '5 000 - 2 730 = ?', 'variant_a': '2 370', 'variant_b': '2 270', 'variant_c': '2 170', 'variant_d': '3 270', 'togri_javob': 'b', 'izoh': '5 000 - 2 730 = 2 270'},
                {'savol_matni': 'Kutubxonada 850 ta kitob bor edi. 275 tasi berildi. Nechta qoldi?', 'variant_a': '575', 'variant_b': '585', 'variant_c': '675', 'variant_d': '525', 'togri_javob': 'a', 'izoh': '850 - 275 = 575 ta kitob qoldi'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

        # 3. Ko'paytirish jadvali
        top = Topshiriq.objects.filter(nomi__icontains="Ko'paytirish").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': '7 × 8 = ?', 'variant_a': '54', 'variant_b': '56', 'variant_c': '58', 'variant_d': '48', 'togri_javob': 'b', 'izoh': '7 × 8 = 56'},
                {'savol_matni': '9 × 6 = ?', 'variant_a': '56', 'variant_b': '52', 'variant_c': '54', 'variant_d': '48', 'togri_javob': 'c', 'izoh': '9 × 6 = 54'},
                {'savol_matni': '12 × 5 = ?', 'variant_a': '50', 'variant_b': '55', 'variant_c': '60', 'variant_d': '65', 'togri_javob': 'c', 'izoh': '12 × 5 = 60. 10×5=50, 2×5=10, 50+10=60'},
                {'savol_matni': '15 × 4 = ?', 'variant_a': '50', 'variant_b': '55', 'variant_c': '60', 'variant_d': '65', 'togri_javob': 'c', 'izoh': '15 × 4 = 60'},
                {'savol_matni': '8 × 9 = ?', 'variant_a': '63', 'variant_b': '72', 'variant_c': '81', 'variant_d': '64', 'togri_javob': 'b', 'izoh': '8 × 9 = 72'},
                {'savol_matni': '25 × 4 = ?', 'variant_a': '80', 'variant_b': '90', 'variant_c': '100', 'variant_d': '120', 'togri_javob': 'c', 'izoh': '25 × 4 = 100'},
                {'savol_matni': '6 × 7 = ?', 'variant_a': '36', 'variant_b': '42', 'variant_c': '48', 'variant_d': '49', 'togri_javob': 'b', 'izoh': '6 × 7 = 42'},
                {'savol_matni': '11 × 11 = ?', 'variant_a': '111', 'variant_b': '121', 'variant_c': '110', 'variant_d': '122', 'togri_javob': 'b', 'izoh': '11 × 11 = 121'},
                {'savol_matni': '50 × 20 = ?', 'variant_a': '100', 'variant_b': '500', 'variant_c': '1 000', 'variant_d': '10 000', 'togri_javob': 'c', 'izoh': '50 × 20: 5 × 2 = 10, keyin 2 ta nol qo\'shamiz = 1 000'},
                {'savol_matni': 'Har bir qatorda 8 ta o\'rindiq bor. 7 ta qator bo\'lsa, jami nechta o\'rindiq?', 'variant_a': '48', 'variant_b': '54', 'variant_c': '56', 'variant_d': '64', 'togri_javob': 'c', 'izoh': '8 × 7 = 56 ta o\'rindiq'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

        # 4. Bo'lish mashqlari
        top = Topshiriq.objects.filter(nomi__icontains="Bo'lish").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': '56 ÷ 8 = ?', 'variant_a': '6', 'variant_b': '7', 'variant_c': '8', 'variant_d': '9', 'togri_javob': 'b', 'izoh': '56 ÷ 8 = 7, chunki 8 × 7 = 56'},
                {'savol_matni': '72 ÷ 9 = ?', 'variant_a': '7', 'variant_b': '8', 'variant_c': '9', 'variant_d': '6', 'togri_javob': 'b', 'izoh': '72 ÷ 9 = 8'},
                {'savol_matni': '100 ÷ 4 = ?', 'variant_a': '20', 'variant_b': '25', 'variant_c': '30', 'variant_d': '50', 'togri_javob': 'b', 'izoh': '100 ÷ 4 = 25'},
                {'savol_matni': '144 ÷ 12 = ?', 'variant_a': '10', 'variant_b': '11', 'variant_c': '12', 'variant_d': '14', 'togri_javob': 'c', 'izoh': '144 ÷ 12 = 12'},
                {'savol_matni': '17 ÷ 5 = ? (qoldiq bilan)', 'variant_a': '3 qoldiq 2', 'variant_b': '3 qoldiq 3', 'variant_c': '2 qoldiq 7', 'variant_d': '4 qoldiq 2', 'togri_javob': 'a', 'izoh': '17 ÷ 5 = 3 qoldiq 2. Tekshirish: 5×3+2=17 ✓'},
                {'savol_matni': '250 ÷ 5 = ?', 'variant_a': '45', 'variant_b': '50', 'variant_c': '55', 'variant_d': '60', 'togri_javob': 'b', 'izoh': '250 ÷ 5 = 50'},
                {'savol_matni': '81 ÷ 9 = ?', 'variant_a': '7', 'variant_b': '8', 'variant_c': '9', 'variant_d': '10', 'togri_javob': 'c', 'izoh': '81 ÷ 9 = 9'},
                {'savol_matni': '630 ÷ 7 = ?', 'variant_a': '80', 'variant_b': '90', 'variant_c': '70', 'variant_d': '100', 'togri_javob': 'b', 'izoh': '630 ÷ 7 = 90'},
                {'savol_matni': '23 ÷ 4 = ? (qoldiq bilan)', 'variant_a': '5 qoldiq 2', 'variant_b': '5 qoldiq 3', 'variant_c': '6 qoldiq 1', 'variant_d': '4 qoldiq 7', 'togri_javob': 'b', 'izoh': '23 ÷ 4 = 5 qoldiq 3. Tekshirish: 4×5+3=23 ✓'},
                {'savol_matni': '96 ta olma 8 ta bolaga teng taqsimlansa, har biriga nechtadan tegadi?', 'variant_a': '10', 'variant_b': '11', 'variant_c': '12', 'variant_d': '14', 'togri_javob': 'c', 'izoh': '96 ÷ 8 = 12 ta olma'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

        # 5. Geometrik shakllar
        top = Topshiriq.objects.filter(nomi__icontains="Geometrik").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': 'Uchburchakning burchaklari yig\'indisi necha gradus?', 'variant_a': '90°', 'variant_b': '180°', 'variant_c': '270°', 'variant_d': '360°', 'togri_javob': 'b', 'izoh': 'Har qanday uchburchakning burchaklari yig\'indisi 180° ga teng.'},
                {'savol_matni': 'Kvadratning barcha tomonlari 5 sm. Perimetri necha sm?', 'variant_a': '15', 'variant_b': '20', 'variant_c': '25', 'variant_d': '10', 'togri_javob': 'b', 'izoh': 'P = 4 × a = 4 × 5 = 20 sm'},
                {'savol_matni': 'Doiraning markazidan chekkagacha bo\'lgan masofaga nima deyiladi?', 'variant_a': 'Diametr', 'variant_b': 'Aylana', 'variant_c': 'Radius', 'variant_d': 'Xorda', 'togri_javob': 'c', 'izoh': 'Radius — markazdan doira chekkasigacha bo\'lgan masofa.'},
                {'savol_matni': 'To\'g\'ri to\'rtburchakning burchagi necha gradus?', 'variant_a': '45°', 'variant_b': '60°', 'variant_c': '90°', 'variant_d': '120°', 'togri_javob': 'c', 'izoh': 'To\'g\'ri to\'rtburchakning har bir burchagi 90°'},
                {'savol_matni': 'Diametr radiusdan necha marta katta?', 'variant_a': '2 marta', 'variant_b': '3 marta', 'variant_c': '4 marta', 'variant_d': 'Teng', 'togri_javob': 'a', 'izoh': 'Diametr = 2 × radius, ya\'ni 2 marta katta.'},
                {'savol_matni': 'To\'g\'ri to\'rtburchakning tomonlari 6 sm va 4 sm. Yuzasi necha sm²?', 'variant_a': '20', 'variant_b': '24', 'variant_c': '10', 'variant_d': '30', 'togri_javob': 'b', 'izoh': 'S = a × b = 6 × 4 = 24 sm²'},
                {'savol_matni': 'Qaysi shakl barcha tomonlari teng va barcha burchaklari 90°?', 'variant_a': 'To\'g\'ri to\'rtburchak', 'variant_b': 'Romb', 'variant_c': 'Kvadrat', 'variant_d': 'Parallelogramm', 'togri_javob': 'c', 'izoh': 'Kvadrat — barcha tomonlari teng va barcha burchaklari 90° bo\'lgan shakl.'},
                {'savol_matni': 'Uchburchakning 2 ta burchagi 50° va 60°. Uchinchi burchak necha gradus?', 'variant_a': '60°', 'variant_b': '70°', 'variant_c': '80°', 'variant_d': '90°', 'togri_javob': 'b', 'izoh': '180° - 50° - 60° = 70°'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

        # 6. Kasrlar sinovi
        top = Topshiriq.objects.filter(nomi__icontains="Kasrlar").first()
        if top and not top.savollar_list.exists():
            savollar = [
                {'savol_matni': '1/4 + 2/4 = ?', 'variant_a': '3/8', 'variant_b': '3/4', 'variant_c': '2/4', 'variant_d': '1/2', 'togri_javob': 'b', 'izoh': 'Maxrajlari teng: 1/4 + 2/4 = (1+2)/4 = 3/4'},
                {'savol_matni': '5/6 - 2/6 = ?', 'variant_a': '3/6', 'variant_b': '3/12', 'variant_c': '7/6', 'variant_d': '2/6', 'togri_javob': 'a', 'izoh': '5/6 - 2/6 = 3/6 = 1/2 (qisqartirilgan holda)'},
                {'savol_matni': '1/3 + 1/6 = ?', 'variant_a': '2/9', 'variant_b': '1/2', 'variant_c': '2/6', 'variant_d': '1/6', 'togri_javob': 'b', 'izoh': 'Umumiy maxraj 6: 1/3 = 2/6. Demak 2/6 + 1/6 = 3/6 = 1/2'},
                {'savol_matni': '2/3 × 3/4 = ?', 'variant_a': '6/12', 'variant_b': '5/7', 'variant_c': '1/2', 'variant_d': '6/7', 'togri_javob': 'c', 'izoh': '2/3 × 3/4 = 6/12 = 1/2'},
                {'savol_matni': '12/18 ni qisqartiring', 'variant_a': '6/9', 'variant_b': '2/3', 'variant_c': '4/6', 'variant_d': '3/4', 'togri_javob': 'b', 'izoh': 'EKUB(12,18) = 6. 12÷6=2, 18÷6=3. Javob: 2/3'},
                {'savol_matni': '3/5 ÷ 1/2 = ?', 'variant_a': '3/10', 'variant_b': '6/5', 'variant_c': '3/7', 'variant_d': '5/6', 'togri_javob': 'b', 'izoh': 'Bo\'lishda ikkinchi kasrni teskari qilamiz: 3/5 × 2/1 = 6/5'},
                {'savol_matni': 'Qaysi kasr eng katta: 1/2, 2/5, 3/4, 1/3?', 'variant_a': '1/2', 'variant_b': '2/5', 'variant_c': '3/4', 'variant_d': '1/3', 'togri_javob': 'c', 'izoh': 'Kasrlarni taqqoslash: 1/2=0,5; 2/5=0,4; 3/4=0,75; 1/3=0,33. Eng kattasi 3/4'},
                {'savol_matni': 'Pitsaning 3/8 qismini yedingiz. Qancha qoldi?', 'variant_a': '5/8', 'variant_b': '3/8', 'variant_c': '4/8', 'variant_d': '6/8', 'togri_javob': 'a', 'izoh': '8/8 - 3/8 = 5/8 qismi qoldi'},
            ]
            for i, s in enumerate(savollar):
                Savol.objects.create(topshiriq=top, tartib=i, **s)

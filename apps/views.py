from functools import wraps
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from .models import (
    Kategoriya, Mavzu, Dars, Topshiriq, Savol, Musobaqa, MusobaqaSavol,
    MusobaqaNatija, ReytingOyinchi,
    KuchsizSoha, HaftalikFaoliyat, Modul, Yutuq, KunlikSovrin,
    OtaOnaMaslahat, UmumiyStatistika, Profil, OquvSozlama,
    BildirishnomaSozlamasi, Tema, XavfsizlikSozlamasi, DarajaSozlamasi,
    SongiFaoliyat, TestNatija,
)


def oqituvchi_talab(view_func):
    """Faqat o'qituvchi roli bo'lgan foydalanuvchilar uchun dekorator."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('kirish')
        if not hasattr(request.user, 'profil') or request.user.profil.rol != 'oqituvchi':
            messages.error(request, "Bu sahifaga faqat o'qituvchilar kira oladi.")
            return redirect('bosh_sahifa')
        return view_func(request, *args, **kwargs)
    return wrapper


def royxatdan_otish(request):
    if request.user.is_authenticated:
        return redirect('bosh_sahifa')

    if request.method == 'POST':
        ism = request.POST.get('ism', '').strip()
        familiya = request.POST.get('familiya', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        parol = request.POST.get('parol', '')
        parol2 = request.POST.get('parol2', '')
        yosh = request.POST.get('yosh', '12')
        sinf = request.POST.get('sinf', '6-sinf')
        maktab = request.POST.get('maktab', '').strip()

        xatolar = []
        if not ism:
            xatolar.append('Ismingizni kiriting')
        if not familiya:
            xatolar.append('Familiyangizni kiriting')
        if not username:
            xatolar.append('Foydalanuvchi nomini kiriting')
        if not email:
            xatolar.append('Email manzilingizni kiriting')
        if len(parol) < 6:
            xatolar.append('Parol kamida 6 ta belgidan iborat bo\'lishi kerak')
        if parol != parol2:
            xatolar.append('Parollar mos kelmadi')
        if User.objects.filter(username=username).exists():
            xatolar.append('Bu foydalanuvchi nomi allaqachon band')
        if User.objects.filter(email=email).exists():
            xatolar.append('Bu email allaqachon ro\'yxatdan o\'tgan')

        if xatolar:
            return render(request, 'royxatdan_otish.html', {
                'xatolar': xatolar,
                'forma': request.POST,
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=parol,
            first_name=ism,
            last_name=familiya,
        )
        Profil.objects.create(
            user=user,
            ism=ism,
            familiya=familiya,
            email=email,
            rol='oquvchi',
            yosh=int(yosh) if yosh.isdigit() else 12,
            sinf=sinf,
            maktab=maktab,
        )
        login(request, user)
        messages.success(request, f'Xush kelibsiz, {ism}! Muvaffaqiyatli ro\'yxatdan o\'tdingiz.')
        return redirect('bosh_sahifa')

    return render(request, 'royxatdan_otish.html')


def kirish(request):
    if request.user.is_authenticated:
        return redirect('bosh_sahifa')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        parol = request.POST.get('parol', '')

        user = authenticate(request, username=username, password=parol)
        if user is not None:
            login(request, user)
            keyingi = request.GET.get('next', 'bosh_sahifa')
            return redirect(keyingi)
        else:
            return render(request, 'kirish.html', {
                'xato': 'Foydalanuvchi nomi yoki parol noto\'g\'ri',
                'username': username,
            })

    return render(request, 'kirish.html')


def chiqish(request):
    logout(request)
    return redirect('kirish')


def bosh_sahifa(request):
    if not request.user.is_authenticated:
        return redirect('royxatdan_otish')
    stat = UmumiyStatistika.get()
    context = {
        'mavzular': Mavzu.objects.all(),
        'kuchsiz_sohalar': KuchsizSoha.objects.all(),
        'musobaqalar': Musobaqa.objects.all(),
        'reyting': ReytingOyinchi.objects.all(),
        'stat': stat,
        'songgi_faoliyat': SongiFaoliyat.objects.filter(sahifa='bosh_sahifa'),
    }
    return render(request, 'bosh_sahifa.html', context)


def darslar(request):
    stat = UmumiyStatistika.get()
    darslar_list = Dars.objects.all()

    tugallangan = darslar_list.filter(holat='tugallangan').count()
    jarayonda = darslar_list.filter(holat='jarayonda').count()
    qolgan = darslar_list.filter(holat='qulflangan').count()

    context = {
        'darslar': darslar_list,
        'sahifalar': [1, 2, 3],
        'joriy_sahifa': 1,
        'stat': stat,
        'tugallangan': tugallangan,
        'jarayonda_soni': jarayonda,
        'qolgan': qolgan,
        'songgi_faoliyat': SongiFaoliyat.objects.filter(sahifa='darslar'),
    }
    return render(request, 'darslar.html', context)


def dars_detail(request, pk):
    dars = get_object_or_404(Dars, pk=pk)
    stat = UmumiyStatistika.get()
    oldingi = Dars.objects.filter(tartib__lt=dars.tartib).order_by('-tartib').first()
    keyingi = Dars.objects.filter(tartib__gt=dars.tartib).order_by('tartib').first()
    topshiriqlar = dars.topshiriqlar.all()
    context = {
        'dars': dars,
        'stat': stat,
        'oldingi': oldingi,
        'keyingi': keyingi,
        'topshiriqlar': topshiriqlar,
    }
    return render(request, 'dars_detail.html', context)


def topshiriqlar(request):
    stat = UmumiyStatistika.get()
    mavzular = Mavzu.objects.prefetch_related('topshiriqlar').all()
    mavzu_topshiriqlar = [
        {'mavzu': m, 'topshiriqlar': m.topshiriqlar.all()}
        for m in mavzular
        if m.topshiriqlar.exists()
    ]
    context = {
        'mavzu_topshiriqlar': mavzu_topshiriqlar,
        'kichik_topshiriqlar': Topshiriq.objects.filter(turi='kichik', mavzu__isnull=True),
        'pastki_topshiriqlar': Topshiriq.objects.filter(turi='pastki', mavzu__isnull=True),
        'stat': stat,
        'songgi_faoliyat': SongiFaoliyat.objects.filter(sahifa='topshiriqlar'),
    }
    return render(request, 'topshiriqlar.html', context)


def topshiriq_detail(request, pk):
    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    stat = UmumiyStatistika.get()
    savollar = topshiriq.savollar_list.all()
    context = {
        'topshiriq': topshiriq,
        'savollar': savollar,
        'stat': stat,
    }
    return render(request, 'topshiriq_detail.html', context)


def topshiriq_tekshirish(request, pk):
    topshiriq = get_object_or_404(Topshiriq, pk=pk)

    if request.method != 'POST':
        return redirect('topshiriq_detail', pk=pk)

    stat = UmumiyStatistika.get()
    savollar = topshiriq.savollar_list.all()

    natijalar = []
    batafsil = []
    togri_soni = 0
    for savol in savollar:
        javob = request.POST.get(f'savol_{savol.pk}', '')
        togri = javob == savol.togri_javob
        if togri:
            togri_soni += 1
        natijalar.append({
            'savol': savol,
            'javob': javob,
            'togri': togri,
        })
        batafsil.append({
            'savol_id': savol.pk,
            'savol_matni': savol.savol_matni,
            'javob': javob,
            'togri_javob': savol.togri_javob,
            'togri': togri,
        })

    umumiy = savollar.count()
    foiz = int((togri_soni / umumiy) * 100) if umumiy > 0 else 0

    # Natijani bazaga saqlash
    TestNatija.objects.create(
        user=request.user if request.user.is_authenticated else None,
        topshiriq=topshiriq,
        togri_soni=togri_soni,
        umumiy_soni=umumiy,
        foiz=foiz,
        batafsil=batafsil,
    )

    # Topshiriq foizini yangilash (oxirgi natija asosida)
    topshiriq.foiz = foiz
    topshiriq.save(update_fields=['foiz'])

    context = {
        'topshiriq': topshiriq,
        'natijalar': natijalar,
        'togri_soni': togri_soni,
        'umumiy': umumiy,
        'foiz': foiz,
        'stat': stat,
    }
    return render(request, 'topshiriq_natija.html', context)


def _haftalik_faoliyat_hisoblash(natijalar_qs):
    """Oxirgi 7 kun ichida har bir kunda yechilgan testlar sonini hisoblaydi."""
    bugun = timezone.localdate()
    boshlanish = bugun - timedelta(days=6)
    kun_nomlari = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya']

    kunlik = (
        natijalar_qs
        .filter(sana__date__gte=boshlanish)
        .annotate(kun=TruncDate('sana'))
        .values('kun')
        .annotate(soni=Count('id'), ort=Avg('foiz'))
    )
    xarita = {k['kun']: k for k in kunlik}

    natija = []
    maks = 1
    for i in range(7):
        sana = boshlanish + timedelta(days=i)
        ma = xarita.get(sana)
        soni = ma['soni'] if ma else 0
        ort = int(ma['ort']) if ma and ma['ort'] is not None else 0
        if soni > maks:
            maks = soni
        natija.append({
            'kun': kun_nomlari[sana.weekday()],
            'sana': sana,
            'testlar': soni,
            'ortacha': ort,
        })

    for d in natija:
        d['foiz'] = int((d['testlar'] / maks) * 100) if maks else 0
    return natija


def _ketma_ket_kun_hisoblash(natijalar_qs):
    """TestNatija asosida ketma-ket faol kunlar sonini topadi (bugungacha)."""
    kunlar = set(
        natijalar_qs.annotate(kun=TruncDate('sana'))
        .values_list('kun', flat=True)
        .distinct()
    )
    if not kunlar:
        return 0
    bugun = timezone.localdate()
    hisob = 0
    joriy = bugun
    if joriy not in kunlar:
        joriy = bugun - timedelta(days=1)
        if joriy not in kunlar:
            return 0
    while joriy in kunlar:
        hisob += 1
        joriy -= timedelta(days=1)
    return hisob


def _modullar_hisoblash():
    """Kategoriyalar bo'yicha o'rtacha test foizini hisoblaydi."""
    ranglar = [
        ('#e8f5e9', '#4caf50'),
        ('#fff3e0', '#ff9800'),
        ('#e3f2fd', '#2196f3'),
        ('#fce4ec', '#e91e63'),
        ('#f3e5f5', '#9c27b0'),
        ('#e0f7fa', '#00bcd4'),
    ]
    ikonlar = ['📐', '➕', '✖️', '📊', '📏', '🔢']

    natija = []
    for i, kat in enumerate(Kategoriya.objects.all()):
        agr = TestNatija.objects.filter(
            topshiriq__dars__kategoriya=kat
        ).aggregate(ort=Avg('foiz'), soni=Count('id'))
        ball = int(agr['ort'] or 0)
        soni = agr['soni'] or 0

        if ball >= 80:
            holat = 'Ajoyib'
        elif ball >= 50:
            holat = "O'rtacha"
        elif soni > 0:
            holat = 'Yaxshilash kerak'
        else:
            holat = 'Boshlanmagan'

        rang, progress_rang = ranglar[i % len(ranglar)]
        natija.append({
            'nomi': kat.nomi,
            'icon': ikonlar[i % len(ikonlar)],
            'rang': rang,
            'progress_rang': progress_rang,
            'ball': ball,
            'urinishlar': soni,
            'holat': holat,
        })
    return natija


def _yutuqlar_hisoblash(natijalar_qs, ketma_ket, ortacha):
    """Foydalanuvchi yutuqlarini dinamik ravishda aniqlaydi."""
    jami = natijalar_qs.count()
    ajoyib_soni = natijalar_qs.filter(foiz__gte=80).count()
    mukammal_soni = natijalar_qs.filter(foiz=100).count()

    shartlar = [
        {
            'nomi': 'Birinchi qadam',
            'tavsif': 'Birinchi testingizni yechdingiz',
            'icon': '🎯',
            'rang': '#e8f5e9',
            'bajarildi': jami >= 1,
        },
        {
            'nomi': "10 ta test yechildi",
            'tavsif': "10 ta testni muvaffaqiyatli bajardingiz",
            'icon': '🏅',
            'rang': '#fff3e0',
            'bajarildi': jami >= 10,
        },
        {
            'nomi': 'Mukammal natija',
            'tavsif': '100% natija bilan test yechdingiz',
            'icon': '⭐',
            'rang': '#fce4ec',
            'bajarildi': mukammal_soni >= 1,
        },
        {
            'nomi': "3 kun ketma-ket",
            'tavsif': '3 kun uzluksiz mashq qildingiz',
            'icon': '🔥',
            'rang': '#e3f2fd',
            'bajarildi': ketma_ket >= 3,
        },
        {
            'nomi': "7 kun ketma-ket",
            'tavsif': 'Bir hafta uzluksiz mashq qildingiz',
            'icon': '🚀',
            'rang': '#f3e5f5',
            'bajarildi': ketma_ket >= 7,
        },
        {
            'nomi': 'A\'lochi',
            'tavsif': "5 tadan ortiq testda 80%+ oldingiz",
            'icon': '🎓',
            'rang': '#e0f7fa',
            'bajarildi': ajoyib_soni >= 5,
        },
    ]
    return [s for s in shartlar if s['bajarildi']]


def statistika(request):
    stat = UmumiyStatistika.get()

    # Foydalanuvchi asosida filter
    if request.user.is_authenticated:
        barcha_natijalar = TestNatija.objects.filter(user=request.user)
    else:
        barcha_natijalar = TestNatija.objects.all()

    oxirgi_natijalar = list(barcha_natijalar[:10])
    jami_testlar = barcha_natijalar.count()
    ortacha_foiz = int(barcha_natijalar.aggregate(avg=Avg('foiz'))['avg'] or 0)
    jami_togri = barcha_natijalar.aggregate(s=Sum('togri_soni'))['s'] or 0
    jami_savollar = barcha_natijalar.aggregate(s=Sum('umumiy_soni'))['s'] or 0
    jami_notogri = max(0, jami_savollar - jami_togri)

    # Natijalar taqsimoti (ajoyib / yaxshi / yomon)
    ajoyib = barcha_natijalar.filter(foiz__gte=80).count()
    yaxshi = barcha_natijalar.filter(foiz__gte=50, foiz__lt=80).count()
    yomon = barcha_natijalar.filter(foiz__lt=50).count()

    # Topshiriq bo'yicha statistika
    topshiriq_stat = []
    for top in Topshiriq.objects.all():
        top_natijalar = barcha_natijalar.filter(topshiriq=top)
        if top_natijalar.exists():
            top_avg = top_natijalar.aggregate(avg=Avg('foiz'))['avg'] or 0
            top_count = top_natijalar.count()
            eng_yaxshi = top_natijalar.order_by('-foiz').first()
            topshiriq_stat.append({
                'topshiriq': top,
                'urinishlar': top_count,
                'ortacha': int(top_avg),
                'eng_yaxshi': eng_yaxshi.foiz if eng_yaxshi else 0,
            })

    # Alohida bloklar
    haftalik = _haftalik_faoliyat_hisoblash(barcha_natijalar)
    ketma_ket = _ketma_ket_kun_hisoblash(barcha_natijalar)
    modullar = _modullar_hisoblash()
    yutuqlar = _yutuqlar_hisoblash(barcha_natijalar, ketma_ket, ortacha_foiz)

    # Chart.js uchun ma'lumotlar
    trend_natijalar = list(reversed(oxirgi_natijalar))
    chart = {
        'haftalik_labels': [d['kun'] for d in haftalik],
        'haftalik_testlar': [d['testlar'] for d in haftalik],
        'haftalik_ortacha': [d['ortacha'] for d in haftalik],
        'modul_labels': [m['nomi'] for m in modullar],
        'modul_ballar': [m['ball'] for m in modullar],
        'modul_ranglar': [m['progress_rang'] for m in modullar],
        'trend_labels': [n.topshiriq.nomi[:14] for n in trend_natijalar],
        'trend_foizlar': [n.foiz for n in trend_natijalar],
        'taqsimot': [ajoyib, yaxshi, yomon],
        'javoblar': [int(jami_togri), int(jami_notogri)],
    }

    context = {
        'haftalik_faoliyat': haftalik,
        'modullar': modullar,
        'yutuqlar': yutuqlar,
        'ota_ona_maslahatlar': OtaOnaMaslahat.objects.all(),
        'stat': stat,
        'ketma_ket_kun': ketma_ket,
        'oxirgi_natijalar': oxirgi_natijalar,
        'jami_testlar': jami_testlar,
        'ortacha_foiz': ortacha_foiz,
        'jami_togri': jami_togri,
        'jami_savollar': jami_savollar,
        'topshiriq_stat': topshiriq_stat,
        'ajoyib_soni': ajoyib,
        'yaxshi_soni': yaxshi,
        'yomon_soni': yomon,
        'chart': chart,
    }
    return render(request, 'statistika.html', context)


def yutuqlar(request):
    stat = UmumiyStatistika.get()
    olinganlar = Yutuq.objects.filter(olingan=True)
    olinmaganlar = Yutuq.objects.filter(olingan=False)

    olingan_soni = olinganlar.count()
    umumiy_soni = Yutuq.objects.count()
    umumiy_ball = sum(y.ball for y in olinganlar)

    darajalar = DarajaSozlamasi.objects.all()
    daraja_nomi = 'Boshlang\'ich'
    daraja_icon = '🌟'
    joriy_ball = umumiy_ball
    kerakli_ball = 500
    daraja_foiz = 0

    for i, d in enumerate(darajalar):
        if umumiy_ball >= d.kerakli_ball:
            daraja_nomi = d.nomi
            daraja_icon = d.icon
            if i + 1 < len(darajalar):
                kerakli_ball = darajalar[i + 1].kerakli_ball
            else:
                kerakli_ball = d.kerakli_ball
        else:
            kerakli_ball = d.kerakli_ball
            break

    if kerakli_ball > 0:
        oldingi_ball = 0
        for d in darajalar:
            if d.kerakli_ball >= kerakli_ball:
                break
            oldingi_ball = d.kerakli_ball
        oraliq = kerakli_ball - oldingi_ball
        if oraliq > 0:
            daraja_foiz = min(100, int(((umumiy_ball - oldingi_ball) / oraliq) * 100))
        else:
            daraja_foiz = 100

    keyingi_daraja_ball = max(0, kerakli_ball - umumiy_ball)
    oxirgi_yutuqlar = olinganlar.order_by('-sana')[:3]

    context = {
        'olinganlar': olinganlar,
        'olinmaganlar': olinmaganlar,
        'kunlik_sovrinlar': KunlikSovrin.objects.all(),
        'oxirgi_yutuqlar': oxirgi_yutuqlar,
        'olingan_yutuqlar': olingan_soni,
        'umumiy_yutuqlar': umumiy_soni,
        'umumiy_ball': umumiy_ball,
        'ketma_ket_kun': stat.ketma_ket_kun,
        'daraja': daraja_nomi,
        'daraja_icon': daraja_icon,
        'daraja_foiz': daraja_foiz,
        'keyingi_daraja_ball': keyingi_daraja_ball,
        'joriy_ball': joriy_ball,
        'kerakli_ball': kerakli_ball,
        'stat': stat,
    }
    return render(request, 'yutuqlar.html', context)


def sozlamalar(request):
    stat = UmumiyStatistika.get()
    profil = None
    if request.user.is_authenticated and hasattr(request.user, 'profil'):
        profil = request.user.profil
    context = {
        'profil': profil,
        'oquv_sozlamalari': OquvSozlama.objects.all(),
        'bildirishnomalar': BildirishnomaSozlamasi.objects.all(),
        'temalar': Tema.objects.all(),
        'xavfsizlik_sozlamalari': XavfsizlikSozlamasi.objects.all(),
        'stat': stat,
        'songgi_faoliyat': SongiFaoliyat.objects.filter(sahifa='sozlamalar'),
    }
    return render(request, 'sozlamalar.html', context)


def _musobaqa_top10(musobaqa):
    """Har bir foydalanuvchining eng yaxshi natijasini olish va top 10 ni qaytarish."""
    from django.db.models import Max
    natijalar = (
        MusobaqaNatija.objects
        .filter(musobaqa=musobaqa, user__isnull=False)
        .values('user__id', 'user__first_name', 'user__last_name', 'user__username')
        .annotate(eng_yaxshi=Max('foiz'))
        .order_by('-eng_yaxshi')[:10]
    )
    top10 = []
    for i, n in enumerate(natijalar):
        ism = n['user__first_name'] or n['user__username']
        familiya = n['user__last_name'] or ''
        top10.append({
            'ism': f"{ism} {familiya}".strip(),
            'foiz': n['eng_yaxshi'],
            'orni': i + 1,
        })
    return top10


def musobaqa_detail(request, pk):
    musobaqa = get_object_or_404(Musobaqa, pk=pk)
    stat = UmumiyStatistika.get()
    savollar = musobaqa.savollar.all()
    top10 = _musobaqa_top10(musobaqa)
    context = {
        'musobaqa': musobaqa,
        'savollar': savollar,
        'stat': stat,
        'top10': top10,
    }
    return render(request, 'musobaqa_detail.html', context)


def musobaqa_tekshirish(request, pk):
    musobaqa = get_object_or_404(Musobaqa, pk=pk)

    if request.method != 'POST':
        return redirect('musobaqa_detail', pk=pk)

    stat = UmumiyStatistika.get()
    savollar = musobaqa.savollar.all()

    natijalar = []
    batafsil = []
    togri_soni = 0
    for savol in savollar:
        javob = request.POST.get(f'savol_{savol.pk}', '')
        togri = javob == savol.togri_javob
        if togri:
            togri_soni += 1
        natijalar.append({
            'savol': savol,
            'javob': javob,
            'togri': togri,
        })
        batafsil.append({
            'savol_id': savol.pk,
            'savol_matni': savol.savol_matni,
            'javob': javob,
            'togri_javob': savol.togri_javob,
            'togri': togri,
        })

    umumiy = savollar.count()
    foiz = int((togri_soni / umumiy) * 100) if umumiy > 0 else 0

    MusobaqaNatija.objects.create(
        user=request.user if request.user.is_authenticated else None,
        musobaqa=musobaqa,
        togri_soni=togri_soni,
        umumiy_soni=umumiy,
        foiz=foiz,
        batafsil=batafsil,
    )

    # Qatnashchilar sonini yangilash
    musobaqa.qatnashchilar = musobaqa.natijalar.count()
    musobaqa.save(update_fields=['qatnashchilar'])

    top10 = _musobaqa_top10(musobaqa)

    context = {
        'musobaqa': musobaqa,
        'natijalar': natijalar,
        'togri_soni': togri_soni,
        'umumiy': umumiy,
        'foiz': foiz,
        'stat': stat,
        'top10': top10,
    }
    return render(request, 'musobaqa_natija.html', context)


# ===================== O'QITUVCHI PANELI =====================

@oqituvchi_talab
def oqituvchi_panel(request):
    """O'qituvchi bosh paneli — umumiy ko'rinish."""
    context = {
        'kategoriyalar_soni': Kategoriya.objects.count(),
        'mavzular_soni': Mavzu.objects.count(),
        'darslar_soni': Dars.objects.count(),
        'topshiriqlar_soni': Topshiriq.objects.count(),
        'savollar_soni': Savol.objects.count(),
        'musobaqalar_soni': Musobaqa.objects.count(),
        'oquvchilar_soni': Profil.objects.filter(rol='oquvchi').count(),
        'testlar_soni': TestNatija.objects.count(),
    }
    return render(request, 'oqituvchi/panel.html', context)


# --- Kategoriya ---
@oqituvchi_talab
def oqituvchi_kategoriyalar(request):
    return render(request, 'oqituvchi/royxat.html', {
        'sarlavha': 'Kategoriyalar',
        'elementlar': Kategoriya.objects.all(),
        'qoshish_url': 'oqituvchi_kategoriya_qoshish',
        'tahrirlash_url': 'oqituvchi_kategoriya_tahrirlash',
        'ochirish_url': 'oqituvchi_kategoriya_ochirish',
        'ustunlar': ['Nomi', 'Tartib'],
        'maydonlar': ['nomi', 'tartib'],
    })


@oqituvchi_talab
def oqituvchi_kategoriya_qoshish(request):
    if request.method == 'POST':
        Kategoriya.objects.create(
            nomi=request.POST.get('nomi', '').strip(),
            tartib=int(request.POST.get('tartib', 0)),
        )
        messages.success(request, 'Kategoriya qo\'shildi.')
        return redirect('oqituvchi_kategoriyalar')
    return render(request, 'oqituvchi/kategoriya_forma.html', {
        'sarlavha': 'Yangi kategoriya',
    })


@oqituvchi_talab
def oqituvchi_kategoriya_tahrirlash(request, pk):
    obj = get_object_or_404(Kategoriya, pk=pk)
    if request.method == 'POST':
        obj.nomi = request.POST.get('nomi', '').strip()
        obj.tartib = int(request.POST.get('tartib', 0))
        obj.save()
        messages.success(request, 'Kategoriya yangilandi.')
        return redirect('oqituvchi_kategoriyalar')
    return render(request, 'oqituvchi/kategoriya_forma.html', {
        'sarlavha': f'"{obj.nomi}" ni tahrirlash',
        'obj': obj,
    })


@oqituvchi_talab
def oqituvchi_kategoriya_ochirish(request, pk):
    obj = get_object_or_404(Kategoriya, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Kategoriya o\'chirildi.')
    return redirect('oqituvchi_kategoriyalar')


# --- Mavzu ---
@oqituvchi_talab
def oqituvchi_mavzular(request):
    return render(request, 'oqituvchi/royxat.html', {
        'sarlavha': 'Mavzular',
        'elementlar': Mavzu.objects.all(),
        'qoshish_url': 'oqituvchi_mavzu_qoshish',
        'tahrirlash_url': 'oqituvchi_mavzu_tahrirlash',
        'ochirish_url': 'oqituvchi_mavzu_ochirish',
        'ustunlar': ['Raqam', 'Nomi', 'Tartib'],
        'maydonlar': ['raqam', 'nomi', 'tartib'],
    })


@oqituvchi_talab
def oqituvchi_mavzu_qoshish(request):
    if request.method == 'POST':
        Mavzu.objects.create(
            raqam=request.POST.get('raqam', '').strip(),
            nomi=request.POST.get('nomi', '').strip(),
            tavsif=request.POST.get('tavsif', '').strip(),
            rang=request.POST.get('rang', '#e8f5e9'),
            icon=request.POST.get('icon', '').strip(),
            tartib=int(request.POST.get('tartib', 0)),
        )
        messages.success(request, 'Mavzu qo\'shildi.')
        return redirect('oqituvchi_mavzular')
    return render(request, 'oqituvchi/mavzu_forma.html', {
        'sarlavha': 'Yangi mavzu',
    })


@oqituvchi_talab
def oqituvchi_mavzu_tahrirlash(request, pk):
    obj = get_object_or_404(Mavzu, pk=pk)
    if request.method == 'POST':
        obj.raqam = request.POST.get('raqam', '').strip()
        obj.nomi = request.POST.get('nomi', '').strip()
        obj.tavsif = request.POST.get('tavsif', '').strip()
        obj.rang = request.POST.get('rang', '#e8f5e9')
        obj.icon = request.POST.get('icon', '').strip()
        obj.tartib = int(request.POST.get('tartib', 0))
        obj.save()
        messages.success(request, 'Mavzu yangilandi.')
        return redirect('oqituvchi_mavzular')
    return render(request, 'oqituvchi/mavzu_forma.html', {
        'sarlavha': f'"{obj.nomi}" ni tahrirlash',
        'obj': obj,
    })


@oqituvchi_talab
def oqituvchi_mavzu_ochirish(request, pk):
    obj = get_object_or_404(Mavzu, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Mavzu o\'chirildi.')
    return redirect('oqituvchi_mavzular')


# --- Dars ---
@oqituvchi_talab
def oqituvchi_darslar(request):
    return render(request, 'oqituvchi/royxat.html', {
        'sarlavha': 'Darslar',
        'elementlar': Dars.objects.all(),
        'qoshish_url': 'oqituvchi_dars_qoshish',
        'tahrirlash_url': 'oqituvchi_dars_tahrirlash',
        'ochirish_url': 'oqituvchi_dars_ochirish',
        'ustunlar': ['Raqam', 'Nomi', 'Kategoriya', 'Holat', 'Tartib'],
        'maydonlar': ['raqam', 'nomi', 'kategoriya', 'holat', 'tartib'],
    })


@oqituvchi_talab
def oqituvchi_dars_qoshish(request):
    if request.method == 'POST':
        kat_pk = request.POST.get('kategoriya')
        kat = Kategoriya.objects.filter(pk=kat_pk).first() if kat_pk else None
        Dars.objects.create(
            raqam=request.POST.get('raqam', '').strip(),
            nomi=request.POST.get('nomi', '').strip(),
            tavsif=request.POST.get('tavsif', '').strip(),
            icon=request.POST.get('icon', '').strip(),
            rang=request.POST.get('rang', '#e8f5e9'),
            davomiylik=request.POST.get('davomiylik', '').strip(),
            holat=request.POST.get('holat', 'qulflangan'),
            kategoriya=kat,
            mazmun=request.POST.get('mazmun', '').strip(),
            tartib=int(request.POST.get('tartib', 0)),
        )
        messages.success(request, 'Dars qo\'shildi.')
        return redirect('oqituvchi_darslar')
    return render(request, 'oqituvchi/dars_forma.html', {
        'sarlavha': 'Yangi dars',
        'kategoriyalar': Kategoriya.objects.all(),
    })


@oqituvchi_talab
def oqituvchi_dars_tahrirlash(request, pk):
    obj = get_object_or_404(Dars, pk=pk)
    if request.method == 'POST':
        kat_pk = request.POST.get('kategoriya')
        obj.raqam = request.POST.get('raqam', '').strip()
        obj.nomi = request.POST.get('nomi', '').strip()
        obj.tavsif = request.POST.get('tavsif', '').strip()
        obj.icon = request.POST.get('icon', '').strip()
        obj.rang = request.POST.get('rang', '#e8f5e9')
        obj.davomiylik = request.POST.get('davomiylik', '').strip()
        obj.holat = request.POST.get('holat', 'qulflangan')
        obj.kategoriya = Kategoriya.objects.filter(pk=kat_pk).first() if kat_pk else None
        obj.mazmun = request.POST.get('mazmun', '').strip()
        obj.tartib = int(request.POST.get('tartib', 0))
        obj.save()
        messages.success(request, 'Dars yangilandi.')
        return redirect('oqituvchi_darslar')
    return render(request, 'oqituvchi/dars_forma.html', {
        'sarlavha': f'"{obj.nomi}" ni tahrirlash',
        'obj': obj,
        'kategoriyalar': Kategoriya.objects.all(),
    })


@oqituvchi_talab
def oqituvchi_dars_ochirish(request, pk):
    obj = get_object_or_404(Dars, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Dars o\'chirildi.')
    return redirect('oqituvchi_darslar')


# --- Topshiriq ---
@oqituvchi_talab
def oqituvchi_topshiriqlar(request):
    return render(request, 'oqituvchi/royxat.html', {
        'sarlavha': 'Topshiriqlar',
        'elementlar': Topshiriq.objects.all(),
        'qoshish_url': 'oqituvchi_topshiriq_qoshish',
        'tahrirlash_url': 'oqituvchi_topshiriq_tahrirlash',
        'ochirish_url': 'oqituvchi_topshiriq_ochirish',
        'ustunlar': ['Nomi', 'Turi', 'Savollar', 'Tartib'],
        'maydonlar': ['nomi', 'turi', 'savollar', 'tartib'],
    })


@oqituvchi_talab
def oqituvchi_topshiriq_qoshish(request):
    if request.method == 'POST':
        topshiriq = Topshiriq.objects.create(
            nomi=request.POST.get('nomi', '').strip(),
            tavsif=request.POST.get('tavsif', '').strip(),
            icon=request.POST.get('icon', 'fas fa-tasks'),
            rang=request.POST.get('rang', '#e8f5e9'),
            turi=request.POST.get('turi', 'kichik'),
            rasm_url=request.POST.get('rasm_url', ''),
            tartib=int(request.POST.get('tartib', 0)),
        )
        messages.success(request, f'"{topshiriq.nomi}" topshirig\'i qo\'shildi.')
        return redirect('oqituvchi_topshiriq_tahrirlash', pk=topshiriq.pk)
    return render(request, 'oqituvchi/topshiriq_forma.html', {
        'sarlavha': "Yangi topshiriq qo'shish",
    })


@oqituvchi_talab
def oqituvchi_topshiriq_tahrirlash(request, pk):
    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    if request.method == 'POST':
        topshiriq.nomi = request.POST.get('nomi', '').strip()
        topshiriq.tavsif = request.POST.get('tavsif', '').strip()
        topshiriq.icon = request.POST.get('icon', 'fas fa-tasks')
        topshiriq.rang = request.POST.get('rang', '#e8f5e9')
        topshiriq.turi = request.POST.get('turi', 'kichik')
        topshiriq.rasm_url = request.POST.get('rasm_url', '')
        topshiriq.tartib = int(request.POST.get('tartib', 0))
        topshiriq.save()
        messages.success(request, f'"{topshiriq.nomi}" topshirig\'i yangilandi.')
        return redirect('oqituvchi_topshiriq_tahrirlash', pk=topshiriq.pk)
    savollar = topshiriq.savollar_list.all()
    return render(request, 'oqituvchi/topshiriq_forma.html', {
        'sarlavha': f'"{topshiriq.nomi}" ni tahrirlash',
        'topshiriq': topshiriq,
        'savollar': savollar,
    })


@oqituvchi_talab
def oqituvchi_topshiriq_ochirish(request, pk):
    topshiriq = get_object_or_404(Topshiriq, pk=pk)
    if request.method == 'POST':
        topshiriq.delete()
        messages.success(request, 'Topshiriq o\'chirildi.')
    return redirect('oqituvchi_topshiriqlar')


# --- Savol (Topshiriq savollari) ---
@oqituvchi_talab
def oqituvchi_savol_qoshish(request, topshiriq_pk):
    topshiriq = get_object_or_404(Topshiriq, pk=topshiriq_pk)
    if request.method == 'POST':
        oxirgi_tartib = topshiriq.savollar_list.count()
        Savol.objects.create(
            topshiriq=topshiriq,
            savol_matni=request.POST.get('savol_matni', '').strip(),
            variant_a=request.POST.get('variant_a', '').strip(),
            variant_b=request.POST.get('variant_b', '').strip(),
            variant_c=request.POST.get('variant_c', '').strip(),
            variant_d=request.POST.get('variant_d', '').strip(),
            togri_javob=request.POST.get('togri_javob', 'a'),
            izoh=request.POST.get('izoh', '').strip(),
            tartib=oxirgi_tartib,
        )
        topshiriq.savollar = topshiriq.savollar_list.count()
        topshiriq.save(update_fields=['savollar'])
        messages.success(request, 'Savol qo\'shildi.')
        return redirect('oqituvchi_topshiriq_tahrirlash', pk=topshiriq.pk)
    return render(request, 'oqituvchi/savol_forma.html', {
        'sarlavha': f'"{topshiriq.nomi}" ga savol qo\'shish',
        'topshiriq': topshiriq,
    })


@oqituvchi_talab
def oqituvchi_savol_tahrirlash(request, pk):
    savol = get_object_or_404(Savol, pk=pk)
    if request.method == 'POST':
        savol.savol_matni = request.POST.get('savol_matni', '').strip()
        savol.variant_a = request.POST.get('variant_a', '').strip()
        savol.variant_b = request.POST.get('variant_b', '').strip()
        savol.variant_c = request.POST.get('variant_c', '').strip()
        savol.variant_d = request.POST.get('variant_d', '').strip()
        savol.togri_javob = request.POST.get('togri_javob', 'a')
        savol.izoh = request.POST.get('izoh', '').strip()
        savol.save()
        messages.success(request, 'Savol yangilandi.')
        return redirect('oqituvchi_topshiriq_tahrirlash', pk=savol.topshiriq.pk)
    return render(request, 'oqituvchi/savol_forma.html', {
        'sarlavha': 'Savolni tahrirlash',
        'topshiriq': savol.topshiriq,
        'savol': savol,
    })


@oqituvchi_talab
def oqituvchi_savol_ochirish(request, pk):
    savol = get_object_or_404(Savol, pk=pk)
    topshiriq = savol.topshiriq
    if request.method == 'POST':
        savol.delete()
        topshiriq.savollar = topshiriq.savollar_list.count()
        topshiriq.save(update_fields=['savollar'])
        messages.success(request, 'Savol o\'chirildi.')
    return redirect('oqituvchi_topshiriq_tahrirlash', pk=topshiriq.pk)


# --- Musobaqa ---
@oqituvchi_talab
def oqituvchi_musobaqalar(request):
    return render(request, 'oqituvchi/royxat.html', {
        'sarlavha': 'Musobaqalar',
        'elementlar': Musobaqa.objects.all(),
        'qoshish_url': 'oqituvchi_musobaqa_qoshish',
        'tahrirlash_url': 'oqituvchi_musobaqa_tahrirlash',
        'ochirish_url': 'oqituvchi_musobaqa_ochirish',
        'ustunlar': ['Nomi', 'Daraja', 'Qatnashchilar', 'Tartib'],
        'maydonlar': ['nomi', 'daraja', 'qatnashchilar', 'tartib'],
    })


@oqituvchi_talab
def oqituvchi_musobaqa_qoshish(request):
    if request.method == 'POST':
        musobaqa = Musobaqa.objects.create(
            nomi=request.POST.get('nomi', '').strip(),
            tavsif=request.POST.get('tavsif', '').strip(),
            icon=request.POST.get('icon', '').strip(),
            rang=request.POST.get('rang', '#e8f5e9'),
            daraja=request.POST.get('daraja', "O'rta"),
            tartib=int(request.POST.get('tartib', 0)),
        )
        messages.success(request, f'"{musobaqa.nomi}" musobaqasi qo\'shildi.')
        return redirect('oqituvchi_musobaqa_tahrirlash', pk=musobaqa.pk)
    return render(request, 'oqituvchi/musobaqa_forma.html', {
        'sarlavha': 'Yangi musobaqa',
    })


@oqituvchi_talab
def oqituvchi_musobaqa_tahrirlash(request, pk):
    obj = get_object_or_404(Musobaqa, pk=pk)
    if request.method == 'POST':
        obj.nomi = request.POST.get('nomi', '').strip()
        obj.tavsif = request.POST.get('tavsif', '').strip()
        obj.icon = request.POST.get('icon', '').strip()
        obj.rang = request.POST.get('rang', '#e8f5e9')
        obj.daraja = request.POST.get('daraja', "O'rta")
        obj.tartib = int(request.POST.get('tartib', 0))
        obj.save()
        messages.success(request, f'"{obj.nomi}" musobaqasi yangilandi.')
        return redirect('oqituvchi_musobaqa_tahrirlash', pk=obj.pk)
    savollar = obj.savollar.all()
    return render(request, 'oqituvchi/musobaqa_forma.html', {
        'sarlavha': f'"{obj.nomi}" ni tahrirlash',
        'obj': obj,
        'savollar': savollar,
    })


@oqituvchi_talab
def oqituvchi_musobaqa_ochirish(request, pk):
    obj = get_object_or_404(Musobaqa, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Musobaqa o\'chirildi.')
    return redirect('oqituvchi_musobaqalar')


# --- Musobaqa savollari ---
@oqituvchi_talab
def oqituvchi_musobaqa_savol_qoshish(request, musobaqa_pk):
    musobaqa = get_object_or_404(Musobaqa, pk=musobaqa_pk)
    if request.method == 'POST':
        oxirgi_tartib = musobaqa.savollar.count()
        MusobaqaSavol.objects.create(
            musobaqa=musobaqa,
            savol_matni=request.POST.get('savol_matni', '').strip(),
            variant_a=request.POST.get('variant_a', '').strip(),
            variant_b=request.POST.get('variant_b', '').strip(),
            variant_c=request.POST.get('variant_c', '').strip(),
            variant_d=request.POST.get('variant_d', '').strip(),
            togri_javob=request.POST.get('togri_javob', 'a'),
            izoh=request.POST.get('izoh', '').strip(),
            tartib=oxirgi_tartib,
        )
        messages.success(request, 'Savol qo\'shildi.')
        return redirect('oqituvchi_musobaqa_tahrirlash', pk=musobaqa.pk)
    return render(request, 'oqituvchi/savol_forma.html', {
        'sarlavha': f'"{musobaqa.nomi}" ga savol qo\'shish',
        'musobaqa': musobaqa,
    })


@oqituvchi_talab
def oqituvchi_musobaqa_savol_tahrirlash(request, pk):
    savol = get_object_or_404(MusobaqaSavol, pk=pk)
    if request.method == 'POST':
        savol.savol_matni = request.POST.get('savol_matni', '').strip()
        savol.variant_a = request.POST.get('variant_a', '').strip()
        savol.variant_b = request.POST.get('variant_b', '').strip()
        savol.variant_c = request.POST.get('variant_c', '').strip()
        savol.variant_d = request.POST.get('variant_d', '').strip()
        savol.togri_javob = request.POST.get('togri_javob', 'a')
        savol.izoh = request.POST.get('izoh', '').strip()
        savol.save()
        messages.success(request, 'Savol yangilandi.')
        return redirect('oqituvchi_musobaqa_tahrirlash', pk=savol.musobaqa.pk)
    return render(request, 'oqituvchi/savol_forma.html', {
        'sarlavha': 'Savolni tahrirlash',
        'musobaqa': savol.musobaqa,
        'savol': savol,
    })


@oqituvchi_talab
def oqituvchi_musobaqa_savol_ochirish(request, pk):
    savol = get_object_or_404(MusobaqaSavol, pk=pk)
    musobaqa = savol.musobaqa
    if request.method == 'POST':
        savol.delete()
        messages.success(request, 'Savol o\'chirildi.')
    return redirect('oqituvchi_musobaqa_tahrirlash', pk=musobaqa.pk)

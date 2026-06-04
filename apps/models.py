from django.db import models
from django.contrib.auth.models import User


class Kategoriya(models.Model):
    nomi = models.CharField(max_length=100)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.nomi


class Mavzu(models.Model):
    raqam = models.CharField(max_length=10)
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    rang = models.CharField(max_length=20, default='#e8f5e9')
    icon = models.CharField(max_length=50)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Mavzu'
        verbose_name_plural = 'Mavzular'

    def __str__(self):
        return f"{self.raqam} - {self.nomi}"


class Dars(models.Model):
    HOLAT_CHOICES = [
        ('tugallangan', 'Tugallangan'),
        ('jarayonda', 'Jarayonda'),
        ('qulflangan', 'Qulflangan'),
    ]
    raqam = models.CharField(max_length=10)
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    davomiylik = models.CharField(max_length=50)
    holat = models.CharField(max_length=20, choices=HOLAT_CHOICES, default='qulflangan')
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.SET_NULL, null=True, blank=True, related_name='darslar')
    tartib = models.PositiveIntegerField(default=0)

    mazmun = models.TextField(blank=True, help_text="Dars matni (HTML yoki oddiy matn)")

    nazariy = models.TextField(blank=True, help_text="Nazariy qism (HTML)")
    taqdimot = models.TextField(blank=True, help_text="Taqdimot matni / slaydlar (HTML)")
    taqdimot_fayl = models.FileField(upload_to='gis/taqdimotlar/', blank=True, null=True, help_text="Taqdimot fayli (.pptx)")
    amaliy_uslubiy = models.TextField(blank=True, help_text="Amaliy-uslubiy ko'rsatma (HTML)")
    topshiriq_matni = models.TextField(blank=True, help_text="Topshiriq matni (HTML)")

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'

    def __str__(self):
        return f"{self.raqam} - {self.nomi}"


class Topshiriq(models.Model):
    TURI_CHOICES = [
        ('kichik', 'Kichik topshiriq'),
        ('pastki', 'Pastki topshiriq'),
    ]
    mavzu = models.ForeignKey(Mavzu, on_delete=models.SET_NULL, null=True, blank=True, related_name='topshiriqlar')
    dars = models.ForeignKey(Dars, on_delete=models.CASCADE, related_name='topshiriqlar', null=True, blank=True)
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    savollar = models.PositiveIntegerField(default=0)
    foiz = models.PositiveIntegerField(default=0)
    progress_rang = models.CharField(max_length=20, blank=True)
    btn_rang = models.CharField(max_length=20, blank=True)
    turi = models.CharField(max_length=20, choices=TURI_CHOICES, default='kichik')
    rasm_url = models.URLField(blank=True)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Topshiriq'
        verbose_name_plural = 'Topshiriqlar'

    def __str__(self):
        return self.nomi


class Savol(models.Model):
    topshiriq = models.ForeignKey(Topshiriq, on_delete=models.CASCADE, related_name='savollar_list')
    savol_matni = models.TextField()
    variant_a = models.CharField(max_length=200)
    variant_b = models.CharField(max_length=200)
    variant_c = models.CharField(max_length=200)
    variant_d = models.CharField(max_length=200)
    togri_javob = models.CharField(max_length=1, choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'),
    ])
    izoh = models.TextField(blank=True, help_text="Javob izohi")
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'

    def __str__(self):
        return f"{self.topshiriq.nomi} - Savol {self.tartib + 1}"


class Musobaqa(models.Model):
    DARAJA_CHOICES = [
        ('Oson', 'Oson'),
        ("O'rta", "O'rta"),
        ('Qiyin', 'Qiyin'),
    ]
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    qatnashchilar = models.PositiveIntegerField(default=0)
    daraja = models.CharField(max_length=20, choices=DARAJA_CHOICES, default="O'rta")
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Musobaqa'
        verbose_name_plural = 'Musobaqalar'

    def __str__(self):
        return self.nomi


class MusobaqaSavol(models.Model):
    musobaqa = models.ForeignKey(Musobaqa, on_delete=models.CASCADE, related_name='savollar')
    savol_matni = models.TextField()
    variant_a = models.CharField(max_length=200)
    variant_b = models.CharField(max_length=200)
    variant_c = models.CharField(max_length=200)
    variant_d = models.CharField(max_length=200)
    togri_javob = models.CharField(max_length=1, choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'),
    ])
    izoh = models.TextField(blank=True, help_text="Javob izohi")
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Musobaqa savoli'
        verbose_name_plural = 'Musobaqa savollari'

    def __str__(self):
        return f"{self.musobaqa.nomi} - Savol {self.tartib + 1}"


class MusobaqaNatija(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='musobaqa_natijalari')
    musobaqa = models.ForeignKey(Musobaqa, on_delete=models.CASCADE, related_name='natijalar')
    togri_soni = models.PositiveIntegerField(default=0)
    umumiy_soni = models.PositiveIntegerField(default=0)
    foiz = models.PositiveIntegerField(default=0)
    sana = models.DateTimeField(auto_now_add=True)
    batafsil = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-sana']
        verbose_name = 'Musobaqa natijasi'
        verbose_name_plural = 'Musobaqa natijalari'

    def __str__(self):
        user_nom = self.user.username if self.user else 'Mehmon'
        return f"{user_nom} - {self.musobaqa.nomi} - {self.foiz}%"


class ReytingOyinchi(models.Model):
    ism = models.CharField(max_length=200)
    ball = models.PositiveIntegerField(default=0)
    medal = models.CharField(max_length=50, blank=True)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Reyting oyinchisi'
        verbose_name_plural = 'Reyting oyinchilari'

    def __str__(self):
        return f"{self.ism} - {self.ball}"


class KuchsizSoha(models.Model):
    nomi = models.CharField(max_length=200)
    foiz = models.PositiveIntegerField(default=0)
    rang = models.CharField(max_length=20, default='#ff7043')
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Kuchsiz soha'
        verbose_name_plural = 'Kuchsiz sohalar'

    def __str__(self):
        return self.nomi


class HaftalikFaoliyat(models.Model):
    kun = models.CharField(max_length=10)
    soat = models.FloatField(default=0)
    foiz = models.PositiveIntegerField(default=0)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Haftalik faoliyat'
        verbose_name_plural = 'Haftalik faoliyatlar'

    def __str__(self):
        return f"{self.kun} - {self.soat} soat"


class Modul(models.Model):
    nomi = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    ball = models.PositiveIntegerField(default=0)
    holat = models.CharField(max_length=50)
    progress_rang = models.CharField(max_length=20, default='#4caf50')
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Modul'
        verbose_name_plural = 'Modullar'

    def __str__(self):
        return f"{self.nomi} - {self.ball}%"


class Yutuq(models.Model):
    nomi = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#fff3e0')
    tavsif = models.TextField()
    ball = models.PositiveIntegerField(default=0)
    sana = models.DateField(null=True, blank=True)
    olingan = models.BooleanField(default=False)
    foiz = models.PositiveIntegerField(default=0, help_text='Faqat olinmagan yutuqlar uchun progress foizi')
    progress_rang = models.CharField(max_length=20, blank=True)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Yutuq'
        verbose_name_plural = 'Yutuqlar'

    def __str__(self):
        holat = 'Olingan' if self.olingan else 'Olinmagan'
        return f"{self.nomi} ({holat})"


class KunlikSovrin(models.Model):
    kun = models.CharField(max_length=10)
    icon = models.CharField(max_length=50)
    ball = models.PositiveIntegerField(default=10)
    olingan = models.BooleanField(default=False)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Kunlik sovrin'
        verbose_name_plural = 'Kunlik sovrinlar'

    def __str__(self):
        return f"{self.kun} - {self.ball} ball"


class OtaOnaMaslahat(models.Model):
    nomi = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    tavsif = models.TextField()
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Ota-ona maslahati'
        verbose_name_plural = 'Ota-ona maslahatlari'

    def __str__(self):
        return self.nomi


class UmumiyStatistika(models.Model):
    umumiy_ball = models.PositiveIntegerField(default=82)
    bajarilgan = models.PositiveIntegerField(default=24)
    jarayonda = models.PositiveIntegerField(default=12)
    umumiy_soat = models.PositiveIntegerField(default=47)
    ketma_ket_kun = models.PositiveIntegerField(default=7)
    ortacha_ball_foiz = models.PositiveIntegerField(default=89)
    yulduzcha = models.PositiveIntegerField(default=150)

    class Meta:
        verbose_name = 'Umumiy statistika'
        verbose_name_plural = 'Umumiy statistika'

    def __str__(self):
        return 'Umumiy statistika'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Profil(models.Model):
    ROL_CHOICES = [
        ('oquvchi', "O'quvchi"),
        ('oqituvchi', "O'qituvchi"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil', null=True, blank=True)
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    email = models.EmailField()
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='oquvchi')
    yosh = models.PositiveIntegerField(default=12)
    sinf = models.CharField(max_length=50, default='6-sinf')
    maktab = models.CharField(max_length=200, default="Umumta'lim maktabi")

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'

    def __str__(self):
        return f"{self.ism} {self.familiya}"


class OquvSozlama(models.Model):
    TURI_CHOICES = [
        ('toggle', 'Toggle'),
        ('select', 'Select'),
    ]
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#e8f5e9')
    icon_rang = models.CharField(max_length=20, default='#4caf50')
    turi = models.CharField(max_length=20, choices=TURI_CHOICES, default='toggle')
    qiymat_bool = models.BooleanField(default=False, help_text='Toggle turi uchun')
    qiymat_text = models.CharField(max_length=100, blank=True, help_text='Select turi uchun')
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = "O'quv sozlamasi"
        verbose_name_plural = "O'quv sozlamalari"

    def __str__(self):
        return self.nomi

    @property
    def qiymat(self):
        if self.turi == 'toggle':
            return self.qiymat_bool
        return self.qiymat_text


class BildirishnomaSozlamasi(models.Model):
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#fff3e0')
    icon_rang = models.CharField(max_length=20, default='#f0a500')
    yoqilgan = models.BooleanField(default=True)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Bildirishnoma sozlamasi'
        verbose_name_plural = 'Bildirishnoma sozlamalari'

    def __str__(self):
        return self.nomi


class Tema(models.Model):
    nomi = models.CharField(max_length=100)
    rang = models.CharField(max_length=20)
    preview_rang = models.CharField(max_length=20)
    tanlangan = models.BooleanField(default=False)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Tema'
        verbose_name_plural = 'Temalar'

    def __str__(self):
        return self.nomi


class XavfsizlikSozlamasi(models.Model):
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField()
    icon = models.CharField(max_length=50)
    rang = models.CharField(max_length=20, default='#fff3e0')
    icon_rang = models.CharField(max_length=20, default='#f0a500')
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Xavfsizlik sozlamasi'
        verbose_name_plural = 'Xavfsizlik sozlamalari'

    def __str__(self):
        return self.nomi


class SongiFaoliyat(models.Model):
    nomi = models.CharField(max_length=200)
    rang = models.CharField(max_length=20, default='#4caf50')
    sahifa = models.CharField(max_length=50, choices=[
        ('bosh_sahifa', 'Bosh sahifa'),
        ('darslar', 'Darslar'),
        ('topshiriqlar', 'Topshiriqlar'),
        ('statistika', 'Statistika'),
        ('yutuqlar', 'Yutuqlar'),
        ('sozlamalar', 'Sozlamalar'),
    ], default='bosh_sahifa', help_text="Qaysi sahifada ko'rinadi")
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = "So'nggi faoliyat"
        verbose_name_plural = "So'nggi faoliyatlar"

    def __str__(self):
        return self.nomi


class TestNatija(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='test_natijalari')
    topshiriq = models.ForeignKey('Topshiriq', on_delete=models.CASCADE, related_name='natijalar')
    togri_soni = models.PositiveIntegerField(default=0)
    umumiy_soni = models.PositiveIntegerField(default=0)
    foiz = models.PositiveIntegerField(default=0)
    sana = models.DateTimeField(auto_now_add=True)
    batafsil = models.JSONField(default=list, blank=True, help_text="Har bir savol natijalari")

    class Meta:
        ordering = ['-sana']
        verbose_name = 'Test natijasi'
        verbose_name_plural = 'Test natijalari'

    def __str__(self):
        user_nom = self.user.username if self.user else 'Mehmon'
        return f"{user_nom} - {self.topshiriq.nomi} - {self.foiz}%"


class DarajaSozlamasi(models.Model):
    nomi = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    kerakli_ball = models.PositiveIntegerField(default=1000)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['tartib']
        verbose_name = 'Daraja'
        verbose_name_plural = 'Darajalar'

    def __str__(self):
        return f"{self.nomi} ({self.kerakli_ball} ball)"

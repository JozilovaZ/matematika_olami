from django.contrib import admin
from .models import (
    Kategoriya, Mavzu, Dars, Topshiriq, Savol, Musobaqa, MusobaqaSavol,
    MusobaqaNatija, ReytingOyinchi,
    KuchsizSoha, HaftalikFaoliyat, Modul, Yutuq, KunlikSovrin,
    OtaOnaMaslahat, UmumiyStatistika, Profil, OquvSozlama,
    BildirishnomaSozlamasi, Tema, XavfsizlikSozlamasi, DarajaSozlamasi,
    SongiFaoliyat, TestNatija, Adabiyot, VideoDars,
)


@admin.register(Adabiyot)
class AdabiyotAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'fayl', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(VideoDars)
class VideoDarsAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'youtube_id', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(Mavzu)
class MavzuAdmin(admin.ModelAdmin):
    list_display = ['raqam', 'nomi', 'icon', 'rang', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(Dars)
class DarsAdmin(admin.ModelAdmin):
    list_display = ['raqam', 'nomi', 'kategoriya', 'davomiylik', 'holat', 'tartib']
    list_editable = ['holat', 'tartib']
    list_filter = ['holat', 'kategoriya']
    search_fields = ['nomi', 'tavsif']
    ordering = ['tartib']


class SavolInline(admin.TabularInline):
    model = Savol
    extra = 1


@admin.register(Topshiriq)
class TopshiriqAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'mavzu', 'dars', 'turi', 'savollar', 'foiz', 'tartib']
    list_editable = ['foiz', 'tartib']
    list_filter = ['turi', 'mavzu', 'dars']
    search_fields = ['nomi']
    ordering = ['tartib']
    inlines = [SavolInline]


@admin.register(Savol)
class SavolAdmin(admin.ModelAdmin):
    list_display = ['topshiriq', 'savol_matni', 'togri_javob', 'tartib']
    list_filter = ['topshiriq']
    ordering = ['topshiriq', 'tartib']


class MusobaqaSavolInline(admin.TabularInline):
    model = MusobaqaSavol
    extra = 1


@admin.register(Musobaqa)
class MusobaqaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'daraja', 'qatnashchilar', 'tartib']
    list_editable = ['qatnashchilar', 'tartib']
    list_filter = ['daraja']
    ordering = ['tartib']
    inlines = [MusobaqaSavolInline]


@admin.register(MusobaqaSavol)
class MusobaqaSavolAdmin(admin.ModelAdmin):
    list_display = ['musobaqa', 'savol_matni', 'togri_javob', 'tartib']
    list_filter = ['musobaqa']
    ordering = ['musobaqa', 'tartib']


@admin.register(MusobaqaNatija)
class MusobaqaNatijaAdmin(admin.ModelAdmin):
    list_display = ['user', 'musobaqa', 'togri_soni', 'umumiy_soni', 'foiz', 'sana']
    list_filter = ['musobaqa', 'sana']
    ordering = ['-sana']


@admin.register(ReytingOyinchi)
class ReytingOyinchiAdmin(admin.ModelAdmin):
    list_display = ['ism', 'ball', 'medal', 'tartib']
    list_editable = ['ball', 'tartib']
    ordering = ['tartib']


@admin.register(KuchsizSoha)
class KuchsizSohaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'foiz', 'rang', 'tartib']
    list_editable = ['foiz', 'tartib']
    ordering = ['tartib']


@admin.register(HaftalikFaoliyat)
class HaftalikFaoliyatAdmin(admin.ModelAdmin):
    list_display = ['kun', 'soat', 'foiz', 'tartib']
    list_editable = ['soat', 'foiz', 'tartib']
    ordering = ['tartib']


@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'ball', 'holat', 'tartib']
    list_editable = ['ball', 'holat', 'tartib']
    ordering = ['tartib']


@admin.register(Yutuq)
class YutuqAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'icon', 'ball', 'olingan', 'sana', 'foiz', 'tartib']
    list_editable = ['ball', 'olingan', 'foiz', 'tartib']
    list_filter = ['olingan']
    search_fields = ['nomi']
    ordering = ['tartib']


@admin.register(KunlikSovrin)
class KunlikSovrinAdmin(admin.ModelAdmin):
    list_display = ['kun', 'icon', 'ball', 'olingan', 'tartib']
    list_editable = ['ball', 'olingan', 'tartib']
    ordering = ['tartib']


@admin.register(OtaOnaMaslahat)
class OtaOnaMaslahatAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'icon', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(UmumiyStatistika)
class UmumiyStatistikaAdmin(admin.ModelAdmin):
    list_display = ['umumiy_ball', 'bajarilgan', 'jarayonda', 'umumiy_soat', 'ketma_ket_kun']

    def has_add_permission(self, request):
        return not UmumiyStatistika.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['ism', 'familiya', 'email', 'rol', 'yosh', 'sinf', 'maktab', 'user']
    list_filter = ['rol', 'sinf']
    list_editable = ['rol']
    search_fields = ['ism', 'familiya', 'email']


@admin.register(OquvSozlama)
class OquvSozlamaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'turi', 'qiymat_bool', 'qiymat_text', 'tartib']
    list_editable = ['qiymat_bool', 'qiymat_text', 'tartib']
    ordering = ['tartib']


@admin.register(BildirishnomaSozlamasi)
class BildirishnomaSozlamasiAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'yoqilgan', 'tartib']
    list_editable = ['yoqilgan', 'tartib']
    ordering = ['tartib']


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'rang', 'preview_rang', 'tanlangan', 'tartib']
    list_editable = ['tanlangan', 'tartib']
    ordering = ['tartib']


@admin.register(XavfsizlikSozlamasi)
class XavfsizlikSozlamasiAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'icon', 'tartib']
    list_editable = ['tartib']
    ordering = ['tartib']


@admin.register(SongiFaoliyat)
class SongiFaoliyatAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'sahifa', 'rang', 'tartib']
    list_editable = ['sahifa', 'tartib']
    list_filter = ['sahifa']
    ordering = ['tartib']


@admin.register(DarajaSozlamasi)
class DarajaSozlamasiAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'icon', 'kerakli_ball', 'tartib']
    list_editable = ['kerakli_ball', 'tartib']
    ordering = ['tartib']


@admin.register(TestNatija)
class TestNatijaAdmin(admin.ModelAdmin):
    list_display = ['user', 'topshiriq', 'togri_soni', 'umumiy_soni', 'foiz', 'sana']
    list_filter = ['topshiriq', 'sana']
    ordering = ['-sana']

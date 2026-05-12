from django.contrib import admin
from django.urls import path
from apps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('darslar/', views.darslar, name='darslar'),
    path('darslar/<int:pk>/', views.dars_detail, name='dars_detail'),
    path('topshiriqlar/', views.topshiriqlar, name='topshiriqlar'),
    path('topshiriqlar/<int:pk>/', views.topshiriq_detail, name='topshiriq_detail'),
    path('topshiriqlar/<int:pk>/tekshirish/', views.topshiriq_tekshirish, name='topshiriq_tekshirish'),
    path('statistika/', views.statistika, name='statistika'),
    path('yutuqlar/', views.yutuqlar, name='yutuqlar'),
    path('sozlamalar/', views.sozlamalar, name='sozlamalar'),
    path('musobaqa/<int:pk>/', views.musobaqa_detail, name='musobaqa_detail'),
    path('musobaqa/<int:pk>/tekshirish/', views.musobaqa_tekshirish, name='musobaqa_tekshirish'),
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),

    # O'qituvchi CRUD
    # Kategoriyalar
    path('oqituvchi/kategoriya/qoshish/', views.oqituvchi_kategoriya_qoshish, name='oqituvchi_kategoriya_qoshish'),
    path('oqituvchi/kategoriya/<int:pk>/tahrirlash/', views.oqituvchi_kategoriya_tahrirlash, name='oqituvchi_kategoriya_tahrirlash'),
    path('oqituvchi/kategoriya/<int:pk>/ochirish/', views.oqituvchi_kategoriya_ochirish, name='oqituvchi_kategoriya_ochirish'),

    # Mavzular
    path('oqituvchi/mavzu/qoshish/', views.oqituvchi_mavzu_qoshish, name='oqituvchi_mavzu_qoshish'),
    path('oqituvchi/mavzu/<int:pk>/tahrirlash/', views.oqituvchi_mavzu_tahrirlash, name='oqituvchi_mavzu_tahrirlash'),
    path('oqituvchi/mavzu/<int:pk>/ochirish/', views.oqituvchi_mavzu_ochirish, name='oqituvchi_mavzu_ochirish'),

    # Darslar
    path('oqituvchi/dars/qoshish/', views.oqituvchi_dars_qoshish, name='oqituvchi_dars_qoshish'),
    path('oqituvchi/dars/<int:pk>/tahrirlash/', views.oqituvchi_dars_tahrirlash, name='oqituvchi_dars_tahrirlash'),
    path('oqituvchi/dars/<int:pk>/ochirish/', views.oqituvchi_dars_ochirish, name='oqituvchi_dars_ochirish'),

    # Topshiriqlar
    path('oqituvchi/topshiriq/qoshish/', views.oqituvchi_topshiriq_qoshish, name='oqituvchi_topshiriq_qoshish'),
    path('oqituvchi/topshiriq/<int:pk>/tahrirlash/', views.oqituvchi_topshiriq_tahrirlash, name='oqituvchi_topshiriq_tahrirlash'),
    path('oqituvchi/topshiriq/<int:pk>/ochirish/', views.oqituvchi_topshiriq_ochirish, name='oqituvchi_topshiriq_ochirish'),
    path('oqituvchi/topshiriq/<int:topshiriq_pk>/savol/qoshish/', views.oqituvchi_savol_qoshish, name='oqituvchi_savol_qoshish'),
    path('oqituvchi/topshiriq/<int:topshiriq_pk>/savol/import/', views.oqituvchi_savollar_import, name='oqituvchi_savollar_import'),
    path('oqituvchi/savol/<int:pk>/tahrirlash/', views.oqituvchi_savol_tahrirlash, name='oqituvchi_savol_tahrirlash'),
    path('oqituvchi/savol/<int:pk>/ochirish/', views.oqituvchi_savol_ochirish, name='oqituvchi_savol_ochirish'),

    # Musobaqalar
    path('oqituvchi/musobaqa/qoshish/', views.oqituvchi_musobaqa_qoshish, name='oqituvchi_musobaqa_qoshish'),
    path('oqituvchi/musobaqa/<int:pk>/tahrirlash/', views.oqituvchi_musobaqa_tahrirlash, name='oqituvchi_musobaqa_tahrirlash'),
    path('oqituvchi/musobaqa/<int:pk>/ochirish/', views.oqituvchi_musobaqa_ochirish, name='oqituvchi_musobaqa_ochirish'),
    path('oqituvchi/musobaqa/<int:musobaqa_pk>/savol/qoshish/', views.oqituvchi_musobaqa_savol_qoshish, name='oqituvchi_musobaqa_savol_qoshish'),
    path('oqituvchi/musobaqa-savol/<int:pk>/tahrirlash/', views.oqituvchi_musobaqa_savol_tahrirlash, name='oqituvchi_musobaqa_savol_tahrirlash'),
    path('oqituvchi/musobaqa-savol/<int:pk>/ochirish/', views.oqituvchi_musobaqa_savol_ochirish, name='oqituvchi_musobaqa_savol_ochirish'),
]

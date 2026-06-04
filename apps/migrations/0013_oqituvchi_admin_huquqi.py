from django.db import migrations


def oqituvchilarga_admin_huquqi(apps, schema_editor):
    Profil = apps.get_model('apps', 'Profil')
    User = apps.get_model('auth', 'User')
    for profil in Profil.objects.filter(rol='oqituvchi', user__isnull=False):
        User.objects.filter(pk=profil.user_id).update(is_staff=True, is_superuser=True)


def orqaga(apps, schema_editor):
    # Ortga qaytarishda o'zgartirmaymiz (xavfsizlik uchun)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_videodars'),
    ]

    operations = [
        migrations.RunPython(oqituvchilarga_admin_huquqi, orqaga),
    ]

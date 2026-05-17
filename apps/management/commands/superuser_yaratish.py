from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.models import Profil


class Command(BaseCommand):
    help = "Superuser yaratish va unga o'qituvchi profili biriktirish"

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help="Foydalanuvchi nomi (default: admin)")
        parser.add_argument('--email', default='admin@example.com', help="Email")
        parser.add_argument('--password', default='admin123', help="Parol (default: admin123)")
        parser.add_argument('--ism', default='Admin', help="Ism")
        parser.add_argument('--familiya', default='', help="Familiya")

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        ism = options['ism']
        familiya = options['familiya']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"'{username}' foydalanuvchisi allaqachon mavjud."))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=ism,
            last_name=familiya,
        )

        if not hasattr(user, 'profil'):
            Profil.objects.create(
                user=user,
                ism=ism,
                familiya=familiya,
                email=email,
                rol='oqituvchi',
            )

        self.stdout.write(self.style.SUCCESS(
            f"Superuser muvaffaqiyatli yaratildi!\n"
            f"  Username : {username}\n"
            f"  Email    : {email}\n"
            f"  Parol    : {password}\n"
            f"  Rol      : o'qituvchi (superuser)"
        ))

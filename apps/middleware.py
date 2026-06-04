from django.shortcuts import redirect


class RoyxatdanOtishMiddleware:
    """Login qilmagan foydalanuvchini avval ro'yxatdan o'tish sahifasiga yo'naltiradi."""

    OCHIQ_YOLLAR = (
        '/royxatdan-otish/',
        '/kirish/',
        '/chiqish/',
        '/admin',
        '/static/',
        '/media/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(self.OCHIQ_YOLLAR):
            return redirect('royxatdan_otish')
        return self.get_response(request)

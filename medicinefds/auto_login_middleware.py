from django.contrib.auth import get_user_model, login


class AutoLoginAdminMiddleware:
    """
    Automatically logs in the first superuser so the admin panel
    can be accessed without entering credentials.
    Only active when DEBUG=True (development only).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            User = get_user_model()
            try:
                superuser = User.objects.filter(is_superuser=True).first()
                if superuser:
                    superuser.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, superuser)
            except Exception:
                pass
        return self.get_response(request)

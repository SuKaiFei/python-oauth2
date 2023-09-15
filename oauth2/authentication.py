from django.contrib.auth.models import User


class ModelBackend:
    is_active = True

    def authenticate(self, request=None, **credentials):
        print(credentials)
        user = User.objects.get()
        user.username = credentials['username']
        user.password = credentials['password']
        return user

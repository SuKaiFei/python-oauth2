from django.contrib.auth.models import User


class ModelBackend:
    is_active = True

    def authenticate(self, request=None, **credentials):
        user = User()
        try:
            user = User.objects.get(username=credentials['username'])
        except User.DoesNotExist as ex:
            user.username = credentials['username']
            user.save()

        return user

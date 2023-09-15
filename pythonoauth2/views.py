from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource


@protected_resource(scopes=['groups'])
def hello_world(request):
    return HttpResponse("hello world")

from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource
import json


@protected_resource(scopes=['groups'])
def hello_world(request):
    name = json.loads(request.body).get("name", "hello world")
    print("Random:", request.headers["Random"])
    print("Timestamps:", request.headers["Timestamps"])
    print("Sign:", request.headers["Sign"])
    print("Authorization:", request.headers["Authorization"])
    return HttpResponse(name)

from django.urls import path, include

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

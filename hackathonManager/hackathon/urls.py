from django.urls import path
from .views import CreateHackathon, ViewHackathon, Enroll


urlpatterns = [
    path('create/', CreateHackathon.as_view(), name='create'),
    path('view/', ViewHackathon.as_view(), name='view'),
    path('enroll/', Enroll.as_view(), name='enroll'),
]

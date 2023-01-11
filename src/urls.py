from django.urls import path
from .views import keywords_view

app_name = 'src'

urlpatterns = [
    path('keywords/', keywords_view, name='keywords'),
]

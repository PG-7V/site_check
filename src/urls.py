from django.urls import path
from .views import keywords_view, RegisterView

app_name = 'src'

urlpatterns = [
    path('keywords/', keywords_view, name='keywords'),
    path('register/', RegisterView.as_view(), name='register'),

]

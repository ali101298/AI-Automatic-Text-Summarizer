from django.urls import path
from .views import summarize_text

urlpatterns = [
    path('', summarize_text, name='home'),
    path('summarize/', summarize_text, name='summarize'),
]
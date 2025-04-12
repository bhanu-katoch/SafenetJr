from django.urls import path
from . import views

urlpatterns = [
    path('view', views.history_view, name='history_view'),
]

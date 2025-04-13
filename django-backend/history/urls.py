from django.urls import path
from . import views

urlpatterns = [
    path('view/<str:child_id>', views.history_view, name='history_view'),
]

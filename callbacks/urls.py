# chat/urls.py
from django.urls import path
from callbacks.views import HomeView, CheckView, CallbackView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    #path("<uuid>", CallbackView.as_view(), name="callback-submit"),
]

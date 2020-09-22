from django.urls import path
from django.conf.urls import include
from callbacks.views import HomeView, CheckView, CallbackView

urlpatterns = [
    path('chat/', include('callbacks.urls')),
    path("check", CheckView.as_view(), name="callback-check"),
    path("<uuid>", CallbackView.as_view(), name="callback-submit"),
    path("<uuid>/<status>", CallbackView.as_view(), name="callback-submit-response"),
    path("", HomeView.as_view(), name="callback-home"),
]

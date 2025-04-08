from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.brevo_webhook_view, name="brevo_webhook"),
]

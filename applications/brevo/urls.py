from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.brevo_webhook_view, name="brevo_webhook"),
    path("events/", views.event_list, name="brevo_event_list"),
    path("events/<str:message_id>/", views.event_detail, name="brevo_event_detail"),
]

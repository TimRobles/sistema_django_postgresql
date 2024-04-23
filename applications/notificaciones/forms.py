from django import forms
from .models import Notificaciones
from bootstrap_modal_forms.forms import BSModalModelForm


# class NotificationForm(BSModalModelForm):
#     class Meta:
#         model = Notificaciones
#         fields = (
#             'titulo',
#             'mensaje')
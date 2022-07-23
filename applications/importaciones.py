from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType

from django.views.generic import (
    TemplateView,
    FormView,
    View,
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    DetailView,
    )
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login, logout

from django.db.models import *

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.template.loader import render_to_string

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalDeleteView,
    BSModalFormView,
    BSModalUpdateView,
    BSModalReadView,
)

from bootstrap_modal_forms.utils import is_ajax
from django.contrib import messages

from django.http import HttpResponse

from .variables import *

from datetime import date, datetime

from django.shortcuts import render

import simplejson

def registro_guardar(form, request):
    if form.created_by == None:
        form.created_by = request.user
    form.updated_by = request.user

def registro_guardar_user(form, usuario):
    if form.created_by == None:
        form.created_by = usuario
    form.updated_by = usuario
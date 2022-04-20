from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model

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

'''from .mixins import *'''

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalDeleteView,
    BSModalFormView,
    BSModalUpdateView,
    BSModalReadView,
)

from bootstrap_modal_forms.utils import is_ajax
from django.contrib import messages

from .variables import *

from django.http import HttpResponse
'''from applications.pdf import generarPDF'''

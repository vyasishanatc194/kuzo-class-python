# -*- coding: utf-8 -*-
from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyView,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.text import Truncator
from django.views.generic import TemplateView
from django_datatables_too.mixins import DataTableMixin

from ..forms import MyGroupForm, MyUserChangeForm, MyUserCreationForm
 

User = get_user_model()

 
 
# -----------------------------------------------------------------------------
# Groups
# -----------------------------------------------------------------------------


class GroupListView(MyListView):
    # paginate_by = 25
    model = Group
    template_name = "core/adminuser/group_list.html"
    permission_required = ("core.view_group",)


class GroupCreateView(MyCreateView):
    model = Group
    form_class = MyGroupForm
    template_name = "core/adminuser/group_form.html"
    permission_required = ("core.add_group",)


class GroupUpdateView(MyUpdateView):
    model = Group
    form_class = MyGroupForm
    template_name = "core/adminuser/group_form.html"
    permission_required = ("core.change_group",)


class GroupDeleteView(MyDeleteView):
    model = Group
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_group",)


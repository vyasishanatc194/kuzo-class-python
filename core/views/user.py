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
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.utils.text import Truncator
from django.views.generic import TemplateView
from django_datatables_too.mixins import DataTableMixin

from ..forms import MyUserChangeForm, MyUserCreationForm

from core.models import User 

import csv

from core.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404




class IndexView(LoginRequiredMixin, TemplateView): 
    template_name = "core/index.html"

    
    def get(self, request):
      
        self.context = {
          
        }
        return render(request, self.template_name, self.context)

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class UserListView(MyListView):
    """
    View for User listing
    """

    paginate_by = 10
    ordering = ["-created_at"]
    model = User
    queryset = model.objects.exclude(username="admin")
    template_name = "core/adminuser/user_list.html"
    permission_required = ("core.view_user",)

    def get_queryset(self):
        
        return self.model.objects.exclude(username="admin").exclude(username=self.request.user)


class UserCreateView(MyCreateView):
    """
    View to create User
    """

    model = User
    form_class = MyUserCreationForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("core.add_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user 
        return kwargs


class UserUpdateView(MyUpdateView):
    """
    View to update User
    """

    model = User
    form_class = MyUserChangeForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UserDeleteView(MyDeleteView):
    """
    View to delete User
    """

    model = User
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_user",)


class UserPasswordView(MyUpdateView):
    """
    View to change User Password
    """
    
    model = User
    form_class = AdminPasswordChangeForm
    template_name = "core/adminuser/password_change_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs


class UserAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = User
    queryset = User.objects.all().order_by("last_name")

    def _get_is_superuser(self, obj):
        """
        Get boolean column markup.
        """
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """
        Get actions column markup.
        """
        # ctx = super().get_context_data(**kwargs)
        t = get_template("core/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """
        Return the list of items for this view.
        """
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(username__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                # | Q(state__icontains=self.search)
                # | Q(year__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data
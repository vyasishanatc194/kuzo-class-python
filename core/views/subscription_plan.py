# -*- coding: utf-8 -*-
from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyView,
    MyNewFormsetUpdateView,
    MyNewFormsetCreateView,
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

from ..forms import SubscriptionPlanForm
from core.models import SubscriptionPlan



# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class SubscriptionPlanListView(MyListView):

    """
    View for SubscriptionPlan listing
    """

    # paginate_by = 25
    ordering = ["id"]
    model = SubscriptionPlan
    queryset = model.objects.all()
    template_name = "core/subscriptionplan/list.html"
    permission_required = ("core.view_subscription_plan",)



class SubscriptionPlanCreateView(MyNewFormsetCreateView):

    """
    View to create SubscriptionPlan
    """

    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = "core/subscriptionplan/form.html"
    permission_required = ("core.add_subscription_plan",)

   

class SubscriptionPlanUpdateView(MyNewFormsetUpdateView):

    """View to update SubscriptionPlan"""

    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = "core/subscriptionplan/form.html"
    permission_required = ("core.change_subscription_plan",)



class SubscriptionPlanDeleteView(MyDeleteView):

    """
    View to delete Subscription Plan
    """

    model = SubscriptionPlan
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_subscription_plan",)


class SubscriptionPlanAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):

    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = SubscriptionPlan
    queryset = SubscriptionPlan.objects.all().order_by("id")

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
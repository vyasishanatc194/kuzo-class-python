# -*- coding: utf-8 -*-
from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyNewFormsetUpdateView,
    MyNewFormsetCreateView,
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from ..forms import EventForm
from core.models import Event



# -----------------------------------------------------------------------------
# Event module
# -----------------------------------------------------------------------------


class EventListView(MyListView):

    """
    View for Offer listing
    """

    # paginate_by = 25
    ordering = ["id"]
    model = Event
    queryset = model.objects.all()
    template_name = "core/event/list.html"
    permission_required = ("core.view_event",)



class EventCreateView(MyNewFormsetCreateView):

    """
    View to create Event
    """

    model = Event
    form_class = EventForm
    template_name = "core/event/form.html"
    permission_required = ("core.add_event",)

   

class EventUpdateView(MyNewFormsetUpdateView):

    """View to update Event """

    model = Event
    form_class = EventForm
    template_name = "core/event/form.html"
    permission_required = ("core.change_event",)



class EventDeleteView(MyDeleteView):

    """
    View to delete Event Plan
    """

    model = Event
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_event",)


class EventAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):

    """
    Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view.
    """

    model = Event
    queryset = Event.objects.all().order_by("id")

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
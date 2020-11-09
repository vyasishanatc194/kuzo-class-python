from django import forms
from core.models import Event, User
from django.utils import timezone
from django.core.exceptions import ValidationError

now = timezone.now()


# -----------------------------------------------------------------------------
# Event
# -----------------------------------------------------------------------------


class EventForm(forms.ModelForm):

    event_date_time = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    """ Custom Event Form"""

    
    def __init__(self,*args,**kwargs):

        super (EventForm,self ).__init__(*args,**kwargs) 
        self.fields['user'].queryset = User.objects.exclude(username="admin")
     

    class Meta():
        model = Event
        fields = [
            
            "user",
            "event_types",
            "about",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "remianing_spots",
            "credit_required",
            "session_lenght",
            "is_featured",
            "is_popular",

            ]

     
    def clean(self):
        cleaned_data = super().clean()
        event_date_time = cleaned_data.get("event_date_time")

        if event_date_time < now:
            raise ValidationError("Event date time should not be past")

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:

            instance.save()

        return instance

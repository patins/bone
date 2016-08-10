from django.forms import ModelForm
from boneweb.models import Resident
from .models import Tinder

class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'picture', 'bio', 'visible']

class TinderForm(ModelForm):
    class Meta:
        model = Tinder
        fields = ['name', 'age', 'location', 'bio', 'picture']

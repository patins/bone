from django.forms import ModelForm
from boneweb.models import Resident, Quote
from .models import Tinder

class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'picture', 'bio', 'visible']

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'public']
        labels = {
          'text': ("Text (no quotation marks!)")
        }

class TinderForm(ModelForm):
    class Meta:
        model = Tinder
        fields = ['name', 'age', 'location', 'bio', 'picture']

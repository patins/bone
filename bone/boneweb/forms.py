from django.forms import ModelForm
from .models import Resident

class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'picture', 'bio', 'visible']

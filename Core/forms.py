from django import forms 
from Core.models import Brain
from .models import BrainImage


class BrainForm(forms.ModelForm):
    class Meta:
        
        model = Brain
        fields = "__all__"
        

class BrainForm(forms.ModelForm):
    class Meta:
        model = BrainImage
        fields = "__all__"
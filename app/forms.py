from django import forms
from .models import *

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'category', 'ingredients', 'imagen']
    
    # Opcionalmente puedes asegurarte de que estos campos no sean requeridos
    rating = forms.FloatField(required=False, initial=0)
    votes = forms.IntegerField(required=False, initial=0)

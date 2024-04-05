# myapp/forms.py
from django import forms
from .models import bruecken_ISK_2022, tunnel_ISK_2022, weichen_ISK_2022, stuetzauwerke_ISK_2022, schallschutzwaende_ISK_2022, bahnuebergaenge_ISK_2022 

MODEL_CHOICES = {
    'Brücken': bruecken_ISK_2022,
    'Tunnel': tunnel_ISK_2022,
    'Weichen': weichen_ISK_2022,
    'Stützbauwerke': stuetzauwerke_ISK_2022,
    'Schallschutzwände': schallschutzwaende_ISK_2022,
    'Bahnübergänge': bahnuebergaenge_ISK_2022
}

BUNDESLAENDER_CHOICES = {
    'BW': 'Baden-Württemberg',
    'BY': 'Bayern',
    'HH': 'Hamburg',
    'SH': 'Schleswig-Holstein',
    'NI': 'Niedersachsen',
    'RP': 'Rheinland-Pfalz',
    'HE': 'Hessen',
    'HB': 'Bremen',
    'SL': 'Saarland',
    'BB': 'Brandenburg',
    'BE': 'Berlin',
    'SN': 'Sachsen',
    'TH': 'Thüringen',
    'ST': 'Sachsen-Anhalt',
    'MV': 'Mecklenburg-Vorpommern',
}



class MultiSelectFilterForm(forms.Form):
    selected_options = forms.MultipleChoiceField(
        choices=[(key, key.capitalize()) for key in MODEL_CHOICES.keys()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Anlagen'
    )
    
    # Field for selecting Bundesländer
    selected_bundeslaender = forms.MultipleChoiceField(
        choices=[(abbr, name) for abbr, name in BUNDESLAENDER_CHOICES.items()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Bundesländer'
    )





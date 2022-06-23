from django import forms

class GanadorForm(forms.Form):
    ticket = forms.CharField()


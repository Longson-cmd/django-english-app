from django import forms


class AddSentenceForm(forms.Form):
    word = forms.CharField(max_length=100)
    sentence = forms.CharField(max_length=1000)
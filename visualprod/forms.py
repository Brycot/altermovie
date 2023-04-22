from django import forms


class RateVideoProduction(forms.Form):
    score_choices = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    rate = forms.ChoiceField(choices=score_choices, widget=forms.Select())

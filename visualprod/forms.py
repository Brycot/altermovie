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


class OrderProductions(forms.Form):
    order_choices = [
        ('name',  'Name (ascending)'),
        ('-name',  'Name (descending)'),
        ('rating', 'Rating (ascending)'),
        ('-rating', 'Rating (descending)'),
        ('number_visualizations', 'Visualizations (ascending)'),
        ('-number_visualizations', 'Visualizations (descending)'),
        ('genre', 'Genre'),
    ]
    order_by = forms.ChoiceField(choices=order_choices, widget=forms.Select())

class SearchProductions(forms.Form):
    search = forms.CharField(max_length=100)
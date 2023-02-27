from django import forms


class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(min_length=2, max_length=255)
    description = forms.CharField(widget=forms.Textarea(), max_length=255)
    rating = forms.FloatField()
    price = forms.FloatField()

class CommentsCreateForm(forms.Form):
    text = forms.CharField(max_length=255)
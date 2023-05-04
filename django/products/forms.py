from django import forms
from .models import Product

input_css_class = "form-contorl"

class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class" : "form-contorl"}))
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "input_css_class"
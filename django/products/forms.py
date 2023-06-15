from django import forms
from .models import Product

input_css_class = "form-control"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': input_css_class}),
            'handle': forms.TextInput(attrs={'class': input_css_class}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
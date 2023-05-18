from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment

input_css_class = "form-control"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class

ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    fields = ['file', 'name', 'is_free', 'active'],
    extra = 0,
    can_delete=False,
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    formset = ProductAttachmentModelFormSet,
    fields = ['file', 'name', 'is_free', 'active'],
    extra = 0,
    can_delete=False,
)
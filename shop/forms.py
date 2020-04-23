from django import forms

from shop.models import Product


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1, label="Количество: ")

    def __init__(self, *args, **kwargs):

        extra = kwargs.pop('extra')
        super().__init__(*args, **kwargs)

        self.obj = Product.objects.get(slug=extra['slug'])

        if self.obj.property:
            for field in self.obj.property:
                CHOICES = []
                for value in self.obj.property[field]:
                    wrap = (value, value)
                    CHOICES.append(wrap)
                self.fields[field] = forms.CharField(label=field,  widget=forms.Select(choices=CHOICES))

        #     for x in field.values_set.all():
        #         a = (x, x)
        #         CHOICES.append(a)
        #     if len(CHOICES) < 6:
        #         self.fields[field.title] = forms.CharField(label=field.title, widget=forms.RadioSelect(choices=CHOICES, attrs={'price': '1111'}))
        #     else:
        #         self.fields[field.title] = forms.CharField(label=field.title, widget=forms.Select(choices=CHOICES))
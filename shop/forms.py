from django import forms
from django.forms.widgets import Select

from shop.models import Product

# class MySelect(Select):
#
#     def __init__(self, attrs=None, choices=(), disabled_choices=()):
#         super(Select, self).__init__(attrs, choices=choices)
#         # disabled_choices is a list of disabled values
#         self.disabled_choices = disabled_choices
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super(Select, self).create_option(name, value, label, selected, index, subindex, attrs)
#         if value in self.disabled_choices:
#             print('============')
#             print(self.disabled_choices)
#             print(value)
#             print('============')
#             option['attrs']['disabled'] = True
#             option['attrs']['price'] = '111'
#         return option


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1, label="Количество: ")

    def __init__(self, *args, **kwargs):

        extra = kwargs.pop('extra')
        super().__init__(*args, **kwargs)

        self.obj = Product.objects.get(slug=extra['slug'])

        if self.obj.property:
            for field in self.obj.property:
                CHOICES = []
                DIS = []
                for value in self.obj.property[field]:
                    # if value == 'Красный' or value == 'Зеленый':
                    #     DIS.append(value)
                    wrap = (value, value)
                    CHOICES.append(wrap)
                self.fields[field] = forms.CharField(label=field,  widget=Select(choices=CHOICES))


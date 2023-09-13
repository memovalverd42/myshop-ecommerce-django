from django import forms
from django.utils.translation import gettext_lazy as _

PORDUCT_QUANTITY_CHOICES = [ (i, str(i)) for i in range(1, 21) ]

class CartAddProductForm(forms.Form):
    '''Modelo para formulario de añadir producto al carrito'''
    
    quantity = forms.TypedChoiceField(choices=PORDUCT_QUANTITY_CHOICES, 
                                      coerce=int,
                                      label=_('Quantity'))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
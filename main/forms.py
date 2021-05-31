from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['order_date'].label = 'Бажана дата отримання замовлення'
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'adress',
            'buying_type',
            'order_date',
            'comment'
        )
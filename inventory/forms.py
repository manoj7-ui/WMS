from django import forms
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        movement_type = cleaned_data.get("movement_type")
        quantity = cleaned_data.get("quantity")
        product = cleaned_data.get("product")

        if movement_type == 'OUT' and product and quantity:
            if quantity > product.current_stock:
                raise forms.ValidationError("Not enough stock available.")

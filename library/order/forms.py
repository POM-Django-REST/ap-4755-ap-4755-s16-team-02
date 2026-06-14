from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user", "book", "plated_end_at"]
        widgets = {
            "plated_end_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            )
        }
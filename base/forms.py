from django.forms import ModelForm, DateField, widgets
from django_flatpickr.widgets import DatePickerInput
from .models import Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "form-control bg-light"
        self.fields["name"].widget.attrs["placeholder"] = "Name the Expense"

        self.fields["description"].widget.attrs["class"] = "form-control bg-light"
        self.fields["description"].widget.attrs["placeholder"] = "Describe the Expense"

        self.fields["category"].widget.attrs["class"] = "form-control bg-light"
        self.fields["category"].widget.attrs[
            "placeholder"
        ] = "Select Category (drop-down)"

        self.fields["data_of_expense"].widget.attrs["class"] = "form-control bg-light"
        self.fields["data_of_expense"].widget.attrs[
            "placeholder"
        ] = "Date of Expense (date-picker)"

        self.fields["amount"].widget.attrs["class"] = "form-control bg-light"
        self.fields["amount"].widget.attrs["placeholder"] = "Expense Amount in INR"

    class Meta:
        model = Expense
        fields = ["name", "data_of_expense", "category", "description", "amount"]
        widgets = {"data_of_expense": widgets.DateInput(attrs={"type": "date"})}

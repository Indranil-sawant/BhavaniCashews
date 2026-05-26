from django import forms
from .models import ShippingAddress

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'email',
            'phone',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'postal_code',
            'country',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': '10-digit mobile number'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'Flat, House no., Building, Company, Apartment'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'Area, Street, Sector, Village (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'City/Town'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': 'State'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'placeholder': '6-digit Pincode'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition duration-150',
                'value': 'India',
                'readonly': 'readonly'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Check standard 10-digit validation
        cleaned = ''.join(filter(str.isdigit, phone))
        if len(cleaned) < 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return cleaned

    def clean_postal_code(self):
        pincode = self.cleaned_data.get('postal_code')
        cleaned = ''.join(filter(str.isdigit, pincode))
        if len(cleaned) != 6:
            raise forms.ValidationError("Pincode must be exactly 6 digits.")
        return cleaned

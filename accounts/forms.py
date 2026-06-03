from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name',
            'phone',
            'address_line1',
            'address_line2',
            'landmark',
            'city',
            'state',
            'pincode',
            'country',
            'is_default'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': '10-digit mobile number'
            }),
            'address_line1': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'Flat, House no., Building, Company, Apartment'
            }),
            'address_line2': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'Area, Street, Sector, Village (optional)'
            }),
            'landmark': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'E.g. Near Apollo Hospital (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'City/Town'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'placeholder': '6-digit Pincode'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant/20 rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-secondary focus:border-secondary focus:bg-surface-container-lowest transition-all',
                'value': 'India',
                'readonly': 'readonly'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = ''.join(filter(str.isdigit, phone))
        if len(cleaned) < 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return cleaned

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        cleaned = ''.join(filter(str.isdigit, pincode))
        if len(cleaned) != 6:
            raise forms.ValidationError("Pincode must be exactly 6 digits.")
        return cleaned

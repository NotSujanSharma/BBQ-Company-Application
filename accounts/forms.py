from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import BBQBooking

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'address']

class BBQBookingForm(forms.ModelForm):
    MAIN_DISHES = BBQBooking.MAIN_DISHES
    SIDE_DISHES = BBQBooking.SIDE_DISHES
    DESSERTS = BBQBooking.DESSERTS

    class Meta:
        model = BBQBooking
        fields = ['date', 'time', 'location', 'guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dish, name in self.MAIN_DISHES:
            self.fields[f'main_dish_{dish}'] = forms.BooleanField(required=False, label=name)
            self.fields[f'main_dish_{dish}_count'] = forms.IntegerField(min_value=0, required=False, initial=0, widget=forms.NumberInput(attrs={'style': 'display:none;'}))
        
        for dish, name in self.SIDE_DISHES:
            self.fields[f'side_dish_{dish}'] = forms.BooleanField(required=False, label=name)
            self.fields[f'side_dish_{dish}_count'] = forms.IntegerField(min_value=0, required=False, initial=0, widget=forms.NumberInput(attrs={'style': 'display:none;'}))
        
        for dessert, name in self.DESSERTS:
            self.fields[f'dessert_{dessert}'] = forms.BooleanField(required=False, label=name)
            self.fields[f'dessert_{dessert}_count'] = forms.IntegerField(min_value=0, required=False, initial=0, widget=forms.NumberInput(attrs={'style': 'display:none;'}))

    def clean(self):
        cleaned_data = super().clean()
        guests = cleaned_data.get('guests')
        if not guests:
            raise forms.ValidationError("Number of guests is required.")

        main_dish_total = sum(cleaned_data.get(f'main_dish_{dish[0]}_count', 0) or 0 for dish in self.MAIN_DISHES if cleaned_data.get(f'main_dish_{dish[0]}'))
        side_dish_total = sum(cleaned_data.get(f'side_dish_{dish[0]}_count', 0) or 0 for dish in self.SIDE_DISHES if cleaned_data.get(f'side_dish_{dish[0]}'))
        dessert_total = sum(cleaned_data.get(f'dessert_{dessert[0]}_count', 0) or 0 for dessert in self.DESSERTS if cleaned_data.get(f'dessert_{dessert[0]}'))

        if main_dish_total != guests:
            raise forms.ValidationError(f"Total main dishes ({main_dish_total}) must equal the number of guests ({guests}).")
        if side_dish_total != guests * 2:
            raise forms.ValidationError(f"Total side dishes ({side_dish_total}) must be twice the number of guests ({guests * 2}).")
        if dessert_total != guests * 2:
            raise forms.ValidationError(f"Total desserts ({dessert_total}) must be twice the number of guests ({guests * 2}).")

        # Set drinks equal to number of guests

        return cleaned_data
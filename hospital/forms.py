from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time_slot', 'symptoms']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10:00 AM'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
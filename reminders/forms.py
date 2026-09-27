from django import forms
from .models import UserProfile, Medicine, Dosage, MedicineSchedule, ReminderLog
import json


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'phone', 'age', 'gender', 'blood_group', 'avatar_color', 'medical_notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 XXXXX XXXXX'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age', 'min': 1, 'max': 120}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. A+, B-, O+'}),
            'avatar_color': forms.Select(attrs={'class': 'form-input'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Any special medical notes...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'category', 'manufacturer', 'description', 'side_effects', 'color_tag', 'requires_prescription']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Medicine Brand Name'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Generic / Chemical Name'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Manufacturer Name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Description of the medicine...'}),
            'side_effects': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Known side effects...'}),
            'color_tag': forms.Select(attrs={'class': 'form-input'}),
            'requires_prescription': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class DosageForm(forms.ModelForm):
    class Meta:
        model = Dosage
        fields = ['medicine', 'dose_quantity', 'unit', 'instructions', 'notes']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-input'}),
            'dose_quantity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-input'}),
            'instructions': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Take after food'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Additional notes...'}),
        }


TIME_SLOT_CHOICES = [
    ('06:00', '6:00 AM'),
    ('07:00', '7:00 AM'),
    ('08:00', '8:00 AM'),
    ('09:00', '9:00 AM'),
    ('10:00', '10:00 AM'),
    ('11:00', '11:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '1:00 PM'),
    ('14:00', '2:00 PM'),
    ('15:00', '3:00 PM'),
    ('16:00', '4:00 PM'),
    ('17:00', '5:00 PM'),
    ('18:00', '6:00 PM'),
    ('19:00', '7:00 PM'),
    ('20:00', '8:00 PM'),
    ('21:00', '9:00 PM'),
    ('22:00', '10:00 PM'),
]


class MedicineScheduleForm(forms.ModelForm):
    time_slots = forms.MultipleChoiceField(
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'time-checkbox'}),
        required=True,
        label='Time Slots'
    )

    class Meta:
        model = MedicineSchedule
        fields = ['user', 'dosage', 'frequency', 'time_slots', 'start_date', 'end_date', 'active', 'prescribed_by']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-input'}),
            'dosage': forms.Select(attrs={'class': 'form-input'}),
            'frequency': forms.Select(attrs={'class': 'form-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'prescribed_by': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dr. Name (optional)'}),
        }

    def clean_time_slots(self):
        return list(self.cleaned_data['time_slots'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate time_slots from existing instance
        if self.instance and self.instance.pk and self.instance.time_slots:
            self.initial['time_slots'] = self.instance.time_slots


class ReminderLogForm(forms.ModelForm):
    class Meta:
        model = ReminderLog
        fields = ['schedule', 'scheduled_time', 'taken_at', 'status', 'notes']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-input'}),
            'scheduled_time': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'taken_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }

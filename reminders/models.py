from django.db import models
from django.utils import timezone


AVATAR_COLORS = [
    ('#06b6d4', 'Teal'),
    ('#8b5cf6', 'Purple'),
    ('#f59e0b', 'Amber'),
    ('#10b981', 'Emerald'),
    ('#ef4444', 'Red'),
    ('#3b82f6', 'Blue'),
    ('#ec4899', 'Pink'),
    ('#f97316', 'Orange'),
]

MEDICINE_CATEGORIES = [
    ('tablet', 'Tablet'),
    ('capsule', 'Capsule'),
    ('syrup', 'Syrup'),
    ('injection', 'Injection'),
    ('drops', 'Drops'),
    ('inhaler', 'Inhaler'),
    ('patch', 'Patch'),
    ('ointment', 'Ointment'),
]

DOSE_UNITS = [
    ('mg', 'mg'),
    ('ml', 'ml'),
    ('tablets', 'Tablets'),
    ('drops', 'Drops'),
    ('puffs', 'Puffs'),
    ('units', 'Units'),
]

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('twice_daily', 'Twice Daily'),
    ('thrice_daily', 'Thrice Daily'),
    ('weekly', 'Weekly'),
    ('alternate', 'Alternate Days'),
    ('as_needed', 'As Needed'),
]

LOG_STATUS = [
    ('taken', 'Taken'),
    ('missed', 'Missed'),
    ('skipped', 'Skipped'),
    ('pending', 'Pending'),
]

COLOR_TAGS = [
    ('#06b6d4', 'Teal'),
    ('#8b5cf6', 'Purple'),
    ('#ef4444', 'Red'),
    ('#10b981', 'Green'),
    ('#f59e0b', 'Amber'),
    ('#3b82f6', 'Blue'),
    ('#ec4899', 'Pink'),
    ('#f97316', 'Orange'),
]


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    avatar_color = models.CharField(max_length=20, choices=AVATAR_COLORS, default='#06b6d4')
    medical_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_initials(self):
        parts = self.name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        return self.name[:2].upper()

    def active_schedules_count(self):
        return self.medicineschedule_set.filter(active=True).count()

    class Meta:
        ordering = ['name']
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=MEDICINE_CATEGORIES, default='tablet')
    manufacturer = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    color_tag = models.CharField(max_length=20, choices=COLOR_TAGS, default='#06b6d4')
    requires_prescription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'


class Dosage(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='dosages')
    dose_quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20, choices=DOSE_UNITS, default='mg')
    instructions = models.CharField(max_length=200, blank=True, help_text="e.g. Take after food, Take with water")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.dose_quantity} {self.unit}"

    class Meta:
        verbose_name = 'Dosage'
        verbose_name_plural = 'Dosages'


class MedicineSchedule(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='medicineschedule_set')
    dosage = models.ForeignKey(Dosage, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    time_slots = models.JSONField(default=list, help_text='List of time strings e.g. ["08:00", "14:00", "21:00"]')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    prescribed_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.dosage.medicine.name} ({self.frequency})"

    def get_time_slots_display(self):
        return ', '.join(self.time_slots) if self.time_slots else 'Not set'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Medicine Schedule'
        verbose_name_plural = 'Medicine Schedules'


class ReminderLog(models.Model):
    schedule = models.ForeignKey(MedicineSchedule, on_delete=models.CASCADE, related_name='logs')
    scheduled_time = models.DateTimeField()
    taken_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=LOG_STATUS, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.schedule.user.name} - {self.schedule.dosage.medicine.name} - {self.status}"

    class Meta:
        ordering = ['-scheduled_time']
        verbose_name = 'Reminder Log'
        verbose_name_plural = 'Reminder Logs'

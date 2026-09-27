from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Medicine, Dosage, MedicineSchedule, ReminderLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('colored_avatar', 'name', 'email', 'phone', 'age', 'gender', 'blood_group', 'active_badge', 'created_at')
    list_filter = ('gender', 'blood_group', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'email', 'phone', 'age', 'gender', 'blood_group')
        }),
        ('Appearance', {
            'fields': ('avatar_color',)
        }),
        ('Medical Notes', {
            'fields': ('medical_notes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )

    def colored_avatar(self, obj):
        initials = obj.get_initials()
        color = obj.avatar_color
        return format_html(
            '<div style="width:36px;height:36px;border-radius:50%;background:{};display:flex;'
            'align-items:center;justify-content:center;color:white;font-weight:bold;font-size:13px;">{}</div>',
            color, initials
        )
    colored_avatar.short_description = ''

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#10b981;color:white;padding:2px 10px;border-radius:20px;font-size:11px;">Active</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 10px;border-radius:20px;font-size:11px;">Inactive</span>')
    active_badge.short_description = 'Status'


class DosageInline(admin.TabularInline):
    model = Dosage
    extra = 1
    fields = ('dose_quantity', 'unit', 'instructions', 'notes')


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('colored_dot', 'name', 'generic_name', 'category_badge', 'manufacturer', 'requires_prescription', 'created_at')
    list_filter = ('category', 'requires_prescription', 'created_at')
    search_fields = ('name', 'generic_name', 'manufacturer')
    readonly_fields = ('created_at',)
    inlines = [DosageInline]
    list_per_page = 20

    fieldsets = (
        ('Medicine Details', {
            'fields': ('name', 'generic_name', 'category', 'manufacturer', 'color_tag')
        }),
        ('Information', {
            'fields': ('description', 'side_effects', 'requires_prescription')
        }),
    )

    def colored_dot(self, obj):
        return format_html(
            '<div style="width:16px;height:16px;border-radius:50%;background:{};display:inline-block;"></div>',
            obj.color_tag
        )
    colored_dot.short_description = ''

    def category_badge(self, obj):
        colors = {
            'tablet': '#3b82f6', 'capsule': '#8b5cf6', 'syrup': '#10b981',
            'injection': '#ef4444', 'drops': '#f59e0b', 'inhaler': '#06b6d4',
            'patch': '#f97316', 'ointment': '#ec4899'
        }
        color = colors.get(obj.category, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:20px;font-size:11px;">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = 'Category'


@admin.register(Dosage)
class DosageAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'dose_quantity', 'unit', 'instructions', 'created_at')
    list_filter = ('unit', 'medicine__category')
    search_fields = ('medicine__name', 'instructions')
    raw_id_fields = ('medicine',)
    list_per_page = 20


@admin.register(MedicineSchedule)
class MedicineScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'medicine_name', 'dosage_info', 'frequency_badge', 'time_display', 'start_date', 'end_date', 'active_badge')
    list_filter = ('frequency', 'active', 'start_date')
    search_fields = ('user__name', 'dosage__medicine__name', 'prescribed_by')
    raw_id_fields = ('user', 'dosage')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        ('Patient & Medicine', {
            'fields': ('user', 'dosage', 'prescribed_by')
        }),
        ('Schedule', {
            'fields': ('frequency', 'time_slots', 'start_date', 'end_date', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def medicine_name(self, obj):
        return obj.dosage.medicine.name
    medicine_name.short_description = 'Medicine'

    def dosage_info(self, obj):
        return f"{obj.dosage.dose_quantity} {obj.dosage.unit}"
    dosage_info.short_description = 'Dosage'

    def frequency_badge(self, obj):
        colors = {
            'daily': '#06b6d4', 'twice_daily': '#8b5cf6', 'thrice_daily': '#f59e0b',
            'weekly': '#10b981', 'alternate': '#3b82f6', 'as_needed': '#6b7280'
        }
        color = colors.get(obj.frequency, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:20px;font-size:11px;">{}</span>',
            color, obj.get_frequency_display()
        )
    frequency_badge.short_description = 'Frequency'

    def time_display(self, obj):
        return obj.get_time_slots_display()
    time_display.short_description = 'Time Slots'

    def active_badge(self, obj):
        if obj.active:
            return format_html('<span style="background:#10b981;color:white;padding:2px 10px;border-radius:20px;font-size:11px;">Active</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 10px;border-radius:20px;font-size:11px;">Inactive</span>')
    active_badge.short_description = 'Status'


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'medicine_name', 'scheduled_time', 'taken_at', 'status_badge', 'notes')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('schedule__user__name', 'schedule__dosage__medicine__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'scheduled_time'
    list_per_page = 25

    def patient_name(self, obj):
        return obj.schedule.user.name
    patient_name.short_description = 'Patient'

    def medicine_name(self, obj):
        return obj.schedule.dosage.medicine.name
    medicine_name.short_description = 'Medicine'

    def status_badge(self, obj):
        colors = {
            'taken': '#10b981', 'missed': '#ef4444',
            'skipped': '#f59e0b', 'pending': '#3b82f6'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:20px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# Customize admin site appearance
admin.site.site_header = '💊 MediRemind Admin'
admin.site.site_title = 'MediRemind'
admin.site.index_title = 'Medicine Reminder System'

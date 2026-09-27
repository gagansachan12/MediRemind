from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import UserProfile, Medicine, Dosage, MedicineSchedule, ReminderLog
from .forms import UserProfileForm, MedicineForm, DosageForm, MedicineScheduleForm, ReminderLogForm


def dashboard(request):
    today = date.today()
    total_users = UserProfile.objects.filter(is_active=True).count()
    total_medicines = Medicine.objects.count()
    active_schedules = MedicineSchedule.objects.filter(active=True).count()
    total_logs = ReminderLog.objects.count()
    taken_today = ReminderLog.objects.filter(status='taken', scheduled_time__date=today).count()
    missed_today = ReminderLog.objects.filter(status='missed', scheduled_time__date=today).count()
    pending_today = ReminderLog.objects.filter(status='pending', scheduled_time__date=today).count()

    # Compliance rate
    total_today = taken_today + missed_today
    compliance_rate = round((taken_today / total_today * 100) if total_today > 0 else 0)

    # Recent logs
    recent_logs = ReminderLog.objects.select_related(
        'schedule__user', 'schedule__dosage__medicine'
    ).order_by('-created_at')[:10]

    # Today's schedules
    todays_schedules = MedicineSchedule.objects.filter(
        active=True,
        start_date__lte=today
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    ).select_related('user', 'dosage__medicine').order_by('user__name')[:12]

    # Recent users
    recent_users = UserProfile.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_medicines': total_medicines,
        'active_schedules': active_schedules,
        'compliance_rate': compliance_rate,
        'taken_today': taken_today,
        'missed_today': missed_today,
        'pending_today': pending_today,
        'recent_logs': recent_logs,
        'todays_schedules': todays_schedules,
        'recent_users': recent_users,
        'today': today,
    }
    return render(request, 'reminders/dashboard.html', context)


# --- Users ---
def user_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    users = UserProfile.objects.all()

    if query:
        users = users.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    users = users.annotate(schedule_count=Count('medicineschedule_set'))

    context = {'users': users, 'query': query, 'status_filter': status_filter, 'total': users.count()}
    return render(request, 'reminders/users.html', context)


def user_add(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Patient "{user.name}" added successfully!')
            return redirect('user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm()
    return render(request, 'reminders/user_form.html', {'form': form, 'title': 'Add New Patient', 'action': 'Add Patient'})


def user_edit(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient "{user.name}" updated successfully!')
            return redirect('user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'reminders/user_form.html', {'form': form, 'title': f'Edit {user.name}', 'action': 'Update Patient', 'user_obj': user})


def user_detail(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    schedules = MedicineSchedule.objects.filter(user=user).select_related('dosage__medicine').order_by('-created_at')
    logs = ReminderLog.objects.filter(schedule__user=user).select_related('schedule__dosage__medicine').order_by('-scheduled_time')[:20]
    taken = logs.filter(status='taken').count()
    missed = logs.filter(status='missed').count()
    compliance = round((taken / (taken + missed) * 100) if (taken + missed) > 0 else 0)
    context = {'user_obj': user, 'schedules': schedules, 'logs': logs, 'compliance': compliance}
    return render(request, 'reminders/user_detail.html', context)


def user_delete(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        name = user.name
        user.delete()
        messages.success(request, f'Patient "{name}" deleted.')
        return redirect('user_list')
    return render(request, 'reminders/confirm_delete.html', {'object': user, 'type': 'Patient'})


# --- Medicines ---
def medicine_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    medicines = Medicine.objects.all()

    if query:
        medicines = medicines.filter(Q(name__icontains=query) | Q(generic_name__icontains=query) | Q(manufacturer__icontains=query))
    if category_filter:
        medicines = medicines.filter(category=category_filter)

    medicines = medicines.annotate(dosage_count=Count('dosages'))

    from .models import MEDICINE_CATEGORIES
    context = {
        'medicines': medicines,
        'query': query,
        'category_filter': category_filter,
        'categories': MEDICINE_CATEGORIES,
        'total': medicines.count()
    }
    return render(request, 'reminders/medicines.html', context)


def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            med = form.save()
            messages.success(request, f'Medicine "{med.name}" added successfully!')
            return redirect('medicine_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MedicineForm()
    return render(request, 'reminders/medicine_form.html', {'form': form, 'title': 'Add New Medicine', 'action': 'Add Medicine'})


def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, f'Medicine "{medicine.name}" updated!')
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'reminders/medicine_form.html', {'form': form, 'title': f'Edit {medicine.name}', 'action': 'Update Medicine', 'med': medicine})


def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        name = medicine.name
        medicine.delete()
        messages.success(request, f'Medicine "{name}" deleted.')
        return redirect('medicine_list')
    return render(request, 'reminders/confirm_delete.html', {'object': medicine, 'type': 'Medicine'})


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    dosages = Dosage.objects.filter(medicine=medicine)
    schedules = MedicineSchedule.objects.filter(dosage__medicine=medicine).select_related('user', 'dosage').order_by('-created_at')[:10]
    context = {'medicine': medicine, 'dosages': dosages, 'schedules': schedules}
    return render(request, 'reminders/medicine_detail.html', context)


# --- Dosages ---
def dosage_add(request):
    if request.method == 'POST':
        form = DosageForm(request.POST)
        if form.is_valid():
            dosage = form.save()
            messages.success(request, f'Dosage for "{dosage.medicine.name}" added!')
            return redirect('medicine_list')
    else:
        medicine_id = request.GET.get('medicine')
        initial = {}
        if medicine_id:
            initial['medicine'] = medicine_id
        form = DosageForm(initial=initial)
    return render(request, 'reminders/dosage_form.html', {'form': form, 'title': 'Add Dosage', 'action': 'Add Dosage'})


# --- Schedules ---
def schedule_list(request):
    query = request.GET.get('q', '')
    active_filter = request.GET.get('active', '')
    schedules = MedicineSchedule.objects.select_related('user', 'dosage__medicine').all()

    if query:
        schedules = schedules.filter(Q(user__name__icontains=query) | Q(dosage__medicine__name__icontains=query))
    if active_filter == 'true':
        schedules = schedules.filter(active=True)
    elif active_filter == 'false':
        schedules = schedules.filter(active=False)

    context = {'schedules': schedules, 'query': query, 'active_filter': active_filter, 'total': schedules.count()}
    return render(request, 'reminders/schedule_list.html', context)


def schedule_add(request):
    if request.method == 'POST':
        form = MedicineScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, f'Schedule created for "{schedule.user.name}"!')
            return redirect('schedule_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MedicineScheduleForm()
    return render(request, 'reminders/schedule_form.html', {'form': form, 'title': 'Create Schedule', 'action': 'Create Schedule'})


def schedule_edit(request, pk):
    schedule = get_object_or_404(MedicineSchedule, pk=pk)
    if request.method == 'POST':
        form = MedicineScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated!')
            return redirect('schedule_list')
    else:
        form = MedicineScheduleForm(instance=schedule)
    return render(request, 'reminders/schedule_form.html', {'form': form, 'title': 'Edit Schedule', 'action': 'Update Schedule'})


def schedule_delete(request, pk):
    schedule = get_object_or_404(MedicineSchedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Schedule deleted.')
        return redirect('schedule_list')
    return render(request, 'reminders/confirm_delete.html', {'object': schedule, 'type': 'Schedule'})


# --- Logs ---
def log_list(request):
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')
    logs = ReminderLog.objects.select_related('schedule__user', 'schedule__dosage__medicine').order_by('-scheduled_time')

    if status_filter:
        logs = logs.filter(status=status_filter)
    if query:
        logs = logs.filter(
            Q(schedule__user__name__icontains=query) |
            Q(schedule__dosage__medicine__name__icontains=query)
        )

    taken = logs.filter(status='taken').count()
    missed = logs.filter(status='missed').count()
    pending = logs.filter(status='pending').count()
    skipped = logs.filter(status='skipped').count()

    context = {
        'logs': logs[:50],
        'taken': taken, 'missed': missed, 'pending': pending, 'skipped': skipped,
        'status_filter': status_filter, 'query': query
    }
    return render(request, 'reminders/log_list.html', context)


def log_update_status(request, pk):
    """AJAX endpoint to mark a reminder as taken/missed/skipped"""
    if request.method == 'POST':
        log = get_object_or_404(ReminderLog, pk=pk)
        status = request.POST.get('status')
        if status in ['taken', 'missed', 'skipped']:
            log.status = status
            if status == 'taken':
                log.taken_at = timezone.now()
            log.save()
            return JsonResponse({'success': True, 'status': status})
    return JsonResponse({'success': False}, status=400)


def generate_todays_reminders(request):
    """Generate reminder log entries for today's active schedules"""
    today = date.today()
    created = 0
    schedules = MedicineSchedule.objects.filter(
        active=True,
        start_date__lte=today
    ).filter(Q(end_date__isnull=True) | Q(end_date__gte=today))

    for schedule in schedules:
        for time_slot in schedule.time_slots:
            hour, minute = map(int, time_slot.split(':'))
            scheduled_dt = timezone.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            scheduled_dt = scheduled_dt.replace(year=today.year, month=today.month, day=today.day)
            _, was_created = ReminderLog.objects.get_or_create(
                schedule=schedule,
                scheduled_time=scheduled_dt,
                defaults={'status': 'pending'}
            )
            if was_created:
                created += 1

    messages.success(request, f'{created} reminder(s) generated for today.')
    return redirect('log_list')

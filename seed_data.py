import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinefds.settings')
import django
django.setup()

from reminders.models import UserProfile, Medicine, Dosage, MedicineSchedule
from datetime import date, timedelta

meds = [
    dict(name='Paracetamol', generic_name='Acetaminophen', category='tablet', manufacturer='GSK', color_tag='#06b6d4', description='Pain reliever and fever reducer'),
    dict(name='Amoxicillin', generic_name='Amoxicillin Trihydrate', category='capsule', manufacturer='Cipla', color_tag='#8b5cf6', requires_prescription=True, description='Antibiotic for bacterial infections'),
    dict(name='Metformin', generic_name='Metformin HCl', category='tablet', manufacturer='Sun Pharma', color_tag='#10b981', requires_prescription=True, description='Used to treat type 2 diabetes'),
    dict(name='Atorvastatin', generic_name='Atorvastatin Calcium', category='tablet', manufacturer='Pfizer', color_tag='#f59e0b', requires_prescription=True, description='Cholesterol lowering medication'),
    dict(name='Omeprazole', generic_name='Omeprazole', category='capsule', manufacturer='AstraZeneca', color_tag='#3b82f6', description='Reduces stomach acid production'),
    dict(name='Cetirizine', generic_name='Cetirizine HCl', category='tablet', manufacturer='UCB', color_tag='#ec4899', description='Antihistamine for allergy relief'),
]

medicines = {}
for md in meds:
    m, created = Medicine.objects.get_or_create(name=md['name'], defaults=md)
    medicines[md['name']] = m

dosage_list = [
    ('Paracetamol', 500, 'mg', 'Take after food'),
    ('Amoxicillin', 500, 'mg', 'Complete full course'),
    ('Metformin', 500, 'mg', 'Take with meals'),
    ('Atorvastatin', 10, 'mg', 'Take at bedtime'),
    ('Omeprazole', 20, 'mg', '30 min before meals'),
    ('Cetirizine', 10, 'mg', 'Once daily'),
]
dosages = {}
for name, qty, unit, instr in dosage_list:
    d, _ = Dosage.objects.get_or_create(
        medicine=medicines[name], dose_quantity=qty, unit=unit,
        defaults={'instructions': instr}
    )
    dosages[name] = d

patients_data = [
    dict(name='Arjun Sharma', email='arjun@example.com', phone='+91 98765 43210', age=45, gender='male', blood_group='B+', avatar_color='#06b6d4', medical_notes='Diabetic patient. Avoid sugary foods.'),
    dict(name='Priya Patel', email='priya@example.com', phone='+91 87654 32109', age=32, gender='female', blood_group='O+', avatar_color='#ec4899', medical_notes='Seasonal allergies.'),
    dict(name='Ravi Kumar', email='ravi@example.com', phone='+91 76543 21098', age=58, gender='male', blood_group='A+', avatar_color='#8b5cf6', medical_notes='Hypertension. Monitor BP regularly.'),
    dict(name='Meera Nair', email='meera@example.com', phone='+91 65432 10987', age=27, gender='female', blood_group='AB-', avatar_color='#10b981', medical_notes='No known allergies.'),
    dict(name='Sanjay Gupta', email='sanjay@example.com', phone='+91 54321 09876', age=62, gender='male', blood_group='O-', avatar_color='#f59e0b', medical_notes='High cholesterol.'),
]
patients = {}
for pd in patients_data:
    p, _ = UserProfile.objects.get_or_create(email=pd['email'], defaults=pd)
    patients[pd['name']] = p

schedule_list = [
    ('Arjun Sharma', 'Metformin', 'twice_daily', ['08:00', '21:00']),
    ('Arjun Sharma', 'Atorvastatin', 'daily', ['21:00']),
    ('Priya Patel', 'Cetirizine', 'daily', ['09:00']),
    ('Ravi Kumar', 'Omeprazole', 'daily', ['07:00']),
    ('Meera Nair', 'Paracetamol', 'thrice_daily', ['08:00', '14:00', '21:00']),
    ('Sanjay Gupta', 'Atorvastatin', 'daily', ['22:00']),
    ('Sanjay Gupta', 'Metformin', 'twice_daily', ['08:00', '20:00']),
]
for pname, mname, freq, slots in schedule_list:
    MedicineSchedule.objects.get_or_create(
        user=patients[pname], dosage=dosages[mname],
        defaults={'frequency': freq, 'time_slots': slots,
                  'start_date': date.today() - timedelta(days=7), 'active': True}
    )

print('Patients:', UserProfile.objects.count())
print('Medicines:', Medicine.objects.count())
print('Dosages:', Dosage.objects.count())
print('Schedules:', MedicineSchedule.objects.count())
print('DONE')

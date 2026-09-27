# 💊 MediRemind — Medicine Reminder & Tracking System

A full-featured Django web application to manage patients, medicines, dosage schedules, and reminder logs — designed for pharmacies, caregivers, and healthcare providers.

---

## 🚀 Features

- 👤 **Patient Management** — Add, edit, and track patient profiles with medical notes, blood group, and contact details
- 💊 **Medicine Catalog** — Maintain a library of medicines with categories, manufacturer info, side effects, and prescription flags
- 📋 **Dosage Tracking** — Define dosage quantities and units (mg, ml, tablets, drops, puffs, etc.) per medicine
- 🗓️ **Schedule Builder** — Set flexible medicine schedules (daily, twice daily, weekly, alternate days, as needed) with custom time slots
- 📊 **Reminder Logs** — Track every dose as Taken, Missed, Skipped, or Pending
- 🌱 **Seed Data Script** — Quickly populate the database with demo patients, medicines, and schedules
- 🔐 **Auto Admin Login Middleware** — Dev-friendly auto-login for quick local testing

---

## 🛠️ Tech Stack

| Layer       | Technology             |
|-------------|------------------------|
| Backend     | Django 6.1             |
| Database    | SQLite (dev)           |
| Frontend    | HTML, CSS, JavaScript  |
| Timezone    | Asia/Kolkata (IST)     |

---

## 📁 Project Structure

```
medicinefds/
├── manage.py
├── seed_data.py              # Demo data population script
├── medicinefds/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── auto_login_middleware.py
│   ├── wsgi.py
│   └── asgi.py
├── reminders/                # Main app
│   ├── models.py             # UserProfile, Medicine, Dosage, MedicineSchedule, ReminderLog
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── templates/
│   └── reminders/            # HTML templates
├── static/
│   ├── css/style.css
│   └── js/main.js
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/gagansachan12/MediRemind.git
cd MediRemind
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install django
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. (Optional) Seed demo data

```bash
python seed_data.py
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit 👉 **http://127.0.0.1:8000/**

---

## 📦 Data Models

| Model              | Description                                              |
|--------------------|----------------------------------------------------------|
| `UserProfile`      | Patient profile with name, contact, gender, blood group  |
| `Medicine`         | Medicine catalog with category, manufacturer, side effects |
| `Dosage`           | Dosage amount + unit linked to a medicine                |
| `MedicineSchedule` | Schedule linking a patient to a dosage with frequency    |
| `ReminderLog`      | Logs each dose event with status (taken/missed/skipped)  |

---

## 🎨 Medicine Categories

`Tablet` · `Capsule` · `Syrup` · `Injection` · `Drops` · `Inhaler` · `Patch` · `Ointment`

## ⏰ Schedule Frequencies

`Daily` · `Twice Daily` · `Thrice Daily` · `Weekly` · `Alternate Days` · `As Needed`

---

## 👨‍💻 Author

**Gagan Sachan**  
📧 gagan8sachan@gmail.com  
🔗 [github.com/gagansachan12](https://github.com/gagansachan12)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --- 1. SABSE PEHLE DOCTOR MODEL (No duplication) ---
class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('General', 'General Physician'),
        ('Pediatrics', 'Pediatrics'),
    ]
    # Ye mapping line hume doctor ko username aur password degi
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES)
    experience = models.IntegerField(help_text="Years of experience", null=True, blank=True)
    email = models.EmailField(default="test@gmail.com")
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"

# --- 2. PATIENT MODEL ---
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# --- 3. TOKEN MODEL ---
class Token(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    token_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token_number} for {self.patient.username}"

# --- 4. APPOINTMENT MODEL ---
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Checked', 'Checked'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=20) # e.g., "10:00 AM - 11:00 AM"
    symptoms = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} ({self.date})"

# --- 5. FEEDBACK MODEL ---
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

# --- 6. AMBULANCE MODEL ---
class Ambulance(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On Mission', 'On Mission'),
    ]
    vehicle_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    updated_at = models.DateTimeField(auto_now=True)
    estimated_arrival = models.CharField(max_length=50, default="10-15 mins")
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.vehicle_number} ({self.current_status})"


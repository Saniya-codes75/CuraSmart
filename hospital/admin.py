from django.contrib import admin
from .models import Doctor, Token, Feedback, Ambulance, Appointment ,Patient  # Appointment yahan add karein

# 1. Doctor Admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')

# 2. Token Admin
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'token_number')
    list_filter = ('doctor',)

# 3. Feedback Admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')

# 4. Ambulance Admin
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'driver_name', 'current_status')

# 5. Appointment Admin (Professional Look)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'status')
    list_filter = ('status', 'date')

# --- SABHI MODELS KO SIRF EK BAAR REGISTER KAREIN ---
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Ambulance, AmbulanceAdmin)
admin.site.register(Appointment, AppointmentAdmin) # Naya Appointment model register ho gaya



# 2. Patient Admin (Taki list mein acchi details dikhein)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'blood_group') # Jo fields aapne model mein banaye hain
    search_fields = ('user__username',) # Search karne ke liye

# 3. Register karein
admin.site.register(Patient, PatientAdmin)
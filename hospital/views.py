from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Doctor, Token, Appointment, Ambulance, Feedback, Patient

# --- 1. DOCTOR & TOKEN SYSTEM ---

def doctor_list(request):
    """Doctors list with Search functionality"""
    query = request.GET.get('search')
    if query:
        doctors = Doctor.objects.filter(name__icontains=query) | Doctor.objects.filter(specialty__icontains=query)
    else:
        doctors = Doctor.objects.all()
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

@login_required
def generate_token(request, doctor_id):
    """Instant Token Generation logic"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    # Aaj ke din ke tokens count karne ke liye (Reset daily logic is better)
    last_token = Token.objects.filter(doctor=doctor).last() 
    new_token_no = (last_token.token_number + 1) if last_token else 1
    
    token = Token.objects.create(
        patient=request.user, 
        doctor=doctor, 
        token_number=new_token_no
    )
    return render(request, 'hospital/token_detail.html', {'token': token})

# --- 2. APPOINTMENT SYSTEM (IMAGE 10 & 11 FIX) ---

@login_required
def book_appointment(request):
    """Booking logic with Validation to prevent Field 'id' expected a number error"""
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        
        # Validation: Agar doctor select nahi kiya toh error na aaye
        if not doctor_id or doctor_id == "":
            messages.error(request, "Please select a valid doctor from the list.")
            return render(request, 'hospital/book_appointment_page.html', {'doctors': doctors})

        try:
            doctor = get_object_or_404(Doctor, id=doctor_id)
            Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                date=request.POST.get('date'),
                time_slot=request.POST.get('time_slot'),
                symptoms=request.POST.get('symptoms'),
                status='Confirmed'
            )
            messages.success(request, "Appointment request sent successfully!")
            return redirect('my_appointments')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return render(request, 'hospital/book_appointment_page.html', {'doctors': doctors})

@login_required
def my_appointments(request):
    """Show booked appointments for current user"""
    appointments = Appointment.objects.filter(patient=request.user).order_by('-id')
    return render(request, 'hospital/my_appointments.html', {'appointments': appointments})

# --- 3. PATIENT DASHBOARD ---

@login_required
def patient_dashboard(request):
    """Unified Dashboard for Tokens and Appointments"""
    my_tokens = Token.objects.filter(patient=request.user).order_by('-id')
    my_apps = Appointment.objects.filter(patient=request.user).order_by('-id')[:5] # Latest 5 apps
    return render(request, 'hospital/dashboard.html', {
        'tokens': my_tokens,
        'appointments': my_apps,
        'latest_token': my_tokens.first()
    })

# --- 4. AUTHENTICATION (IMAGE 4 & 8 FIX) ---

def signup(request):
    """Signup with automatic Patient profile creation"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatic Patient Profile create karega Admin panel ke liye
            Patient.objects.get_or_create(user=user) 
            login(request, user)
            messages.success(request, "Account created! You are now logged in as a Patient.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    # Path changed to hospital/signup.html based on your file structure
    return render(request, 'hospital/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# --- 5. UTILITIES ---

def bmi_calculator(request):
    bmi, category, color = None, "", ""
    if request.method == "POST":
        try:
            weight = float(request.POST.get('weight', 0))
            height = float(request.POST.get('height', 0)) / 100
            if height > 0:
                bmi = round(weight / (height * height), 1)
                if bmi < 18.5: category, color = "Underweight", "#ffc107"
                elif bmi < 25: category, color = "Normal Weight", "#28a745"
                elif bmi < 30: category, color = "Overweight", "#fd7e14"
                else: category, color = "Obese", "#dc3545"
        except (ValueError, ZeroDivisionError):
            messages.error(request, "Invalid input in BMI calculator.")
            
    return render(request, 'hospital/bmi.html', {'bmi': bmi, 'category': category, 'color': color})

def ambulance_list(request):
    ambulances = Ambulance.objects.all()
    return render(request, 'hospital/ambulance_list.html', {'ambulances': ambulances})

@login_required
def submit_feedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            user=request.user, 
            subject=request.POST.get('subject'), 
            message=request.POST.get('message')
        )
        messages.success(request, "Thank you for your valuable feedback!")
        return redirect('doctor_list')
    return render(request, 'hospital/feedback.html')
@login_required
def doctor_dashboard(request):
    """Professional Doctor Dashboard with statistics and profile"""
    try:
        doctor = request.user.doctor
    except (Doctor.DoesNotExist, AttributeError):
        messages.error(request, "Access denied. Only doctors can view this panel.")
        return redirect('doctor_list')

    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')
    
    # Dashboard Analytics (Inhe cards me dikhayenge)
    total_appointments = appointments.count()
    pending_appointments = appointments.filter(status='Pending').count()
    confirmed_appointments = appointments.filter(status='Confirmed').count()

    if request.method == 'POST':
        app_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        
        try:
            appointment = Appointment.objects.get(id=app_id, doctor=doctor)
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment status updated to {new_status}!")
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
            
        return redirect('doctor_dashboard')

    return render(request, 'hospital/doctor_dashboard.html', {
        'appointments': appointments, 
        'doctor': doctor,
        'total_apps': total_appointments,
        'pending_apps': pending_appointments,
        'confirmed_apps': confirmed_appointments
    })
# @login_required
# def doctor_dashboard(request):
#     """Doctor dashboard to view patients and update appointment status"""
#     # 1. Check karein ki login karne wala user Doctor mapped hai ya nahi
#     try:
#         doctor = request.user.doctor
#     except (Doctor.DoesNotExist, AttributeError):
#         messages.error(request, "Access denied. Only doctors can view this panel.")
#         return redirect('doctor_list')

#     # 2. Is doctor ke saare appointments fetch karein (Patient details ke saath)
#     appointments = Appointment.objects.filter(doctor=doctor).order_by('-date')

#     # 3. Agar status update ka form submit hota hai
#     if request.method == 'POST':
#         app_id = request.POST.get('appointment_id')
#         new_status = request.POST.get('status')
        
#         try:
#             appointment = Appointment.objects.get(id=app_id, doctor=doctor)
#             appointment.status = new_status
#             appointment.save()
#             messages.success(request, f"Appointment status updated to {new_status}!")
#         except Appointment.DoesNotExist:
#             messages.error(request, "Appointment not found.")
            
#         return redirect('doctor_dashboard')

#     return render(request, 'hospital/doctor_dashboard.html', {
#         'appointments': appointments, 
#         'doctor': doctor
    # })
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def login_redirect_dispatch(request):
    """
    Login ke baad yeh view decide karega ki user Doctor hai ya Patient,
    Aur URL matching errors se bachne ke liye direct hard path use karega.
    """
    # 1. Check karein ki user Doctor hai ya nahi
    try:
        if request.user.is_staff or (hasattr(request.user, 'doctor') and request.user.doctor is not None):
            return redirect('/doctor/dashboard/')  # Direct doctor dashboard path
    except Exception:
        pass

    # 2. Agar doctor nahi hai, toh use default doctors list par bhej do
    return redirect('/doctors/')  # Direct patient doctor-list path

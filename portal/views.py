from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AppointmentForm
from .models import Appointment, Patient, Message, Doctor
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

# ======== views ========
def home_view(request):
    print("=== LOADING home_view ===")
    return render(request, 'portal/home.html')

@login_required
def appointment_list_view(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    return render(request, 'portal/appointments.html', {'appointments': appointments})

@login_required
def dashboard_view(request):
    print("==== LOADING DASHBOARD VIEW ====")

    # Try to match to a patient
    try:
        patient = Patient.objects.get(user=request.user)
        upcoming = (
            Appointment.objects.filter(patient=patient, appointment_date__gte=now())
            .order_by('appointment_date')
            .first()
        )
        context = {'patient': patient, 'next_appointment': upcoming}
        return render(request, 'portal/patient_dashboard.html', context)
    except Patient.DoesNotExist:
        pass

    # Try to match to a doctor
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=now()
        ).order_by('appointment_date')

        messages = Message.objects.filter(sender=doctor).order_by('-sent_at')

        context = {'doctor': doctor, 
                   'appointments': appointments, 
                   'messages': messages 
                }
        return render(request, 'portal/doctor_dashboard.html', context)
    except Doctor.DoesNotExist:
        return HttpResponse("Unauthorized access: no matching user role.")

@login_required
def appointment_create_view(request):
    patient = Patient.objects.get(user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('/dashboard/')
    else:
        form = AppointmentForm()
    
    return render(request, 'portal/appointment_form.html', {'form': form})

@login_required
def message_list_view(request):
    patient = Patient.objects.get(user=request.user)
    messages = Message.objects.filter(recipient=patient).order_by('-sent_at')

    return render(request, 'portal/messages.html', {'messages': messages})

@login_required
def doctor_patients_view(request):
    doctor = Doctor.objects.get(user=request.user)
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()

    return render(request, 'portal/doctor_patients.html', {'patients': patients})

@login_required
def edit_notes_view(request, appointment_id):
    doctor = Doctor.objects.get(user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        appointment.notes = notes
        appointment.save()
        messages.success(request, "Notes updated successfully.")
        return redirect('dashboard')
    
    return render(request, "portal/edit_notes.html", {'appointment': appointment})
        

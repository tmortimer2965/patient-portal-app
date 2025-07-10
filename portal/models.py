from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"
    

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateTimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} @ {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"


class Message(models.Model):
    sender = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.recipient} from {self.sender} ({self.subject})"

from django.contrib import admin
from .models import Patient, Appointment, Doctor, Message

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__first_name', 'doctor__last_name', 'reason')



admin.site.register(Patient)
#admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Message)
admin.site.register(Appointment, AppointmentAdmin)


from .models import Appointment


def appointments(request):
    if request.user.is_authenticated:
        # Filter appointments for the authenticated user where is_booked is false
        unbooked_appointments = Appointment.objects.filter(author=request.user, is_booked=False)
    else:
        unbooked_appointments = None

    return {'unbooked_appointments': unbooked_appointments}

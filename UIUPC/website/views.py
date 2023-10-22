from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RegistrationRequest
from UIUPC import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Notice, FAQ, Event

def home(request):
    recent_notices = Notice.objects.order_by('-created_at')[:2]
    recent_events = Event.objects.order_by('-created_at')[:4]
    return render(request, 'home.html', {'recent_notices': recent_notices, 'recent_events': recent_events})

def registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        idnumber = request.POST['idnumber']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        department = request.POST['department']
        dob = request.POST['dob']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'The email address is already in use.Please try with another email.')
            return redirect('registration')

        user = User.objects.create_user(username=email, password=firstname, is_active = False)
        new_request = RegistrationRequest(
            email=email,
            idnumber=idnumber,
            firstname=firstname,
            lastname=lastname,
            department=department,
            dob=dob
        )
        new_request.save()
        messages.error(request, 'Thank you for completing the registration. We will send you a confirmation email soon.')

        #Welcoming Email
        subject = "Welcome To UIU Photography Club"
        message = f"Dear {firstname} {lastname},\nThank you for registering at UIUPC, we will contact you soon after reviewing your registration information.\n\nThanks for your patience--Team Meta"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)
        return redirect('registration')
    else:
        return render(request, 'registration.html', {})


def faqs(request):
    faqs = FAQ.objects.all()
    return render(request,'faqs.html', {'faqs':faqs})


def events(request):
    events = Event.objects.all()
    for event in events:
        time_difference = timezone.now() - event.created_at
        event.time_since_creation = time_difference.total_seconds() / 60
    return render(request, 'events.html', {'events':events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})

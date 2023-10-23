from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RegistrationRequest, EventRequest, Notice, FAQ, Event
from UIUPC import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

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
        existing_participants = EventRequest.objects.filter(email=email)
        if User.objects.filter(username=email).exists() or existing_participants.exists() :
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
        message = f"Dear {firstname} {lastname},\n\nThank you for registering at UIU Photography Club. We have received your registration information and will review it shortly.\n\nYour patience is appreciated as we process your request. If you have any questions or need further information, feel free to reach out to us.\n\nBest regards,\nTeam UIU Photography Club"
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
    events = Event.objects.order_by('-created_at')

    for event in events:
        time_difference = timezone.now() - event.created_at
        minutes_since_creation = int(time_difference.total_seconds() / 60)

        if minutes_since_creation < 60:
            event.time_since_creation = f"{minutes_since_creation} minutes ago"
        elif minutes_since_creation < 1440:
            hours_since_creation = minutes_since_creation // 60
            event.time_since_creation = f"{hours_since_creation} hours ago"
        else:
            days_since_creation = minutes_since_creation // 1440
            event.time_since_creation = f"{days_since_creation} days ago"

    return render(request, 'events.html', {'events': events})

def event_detail(request, e_id):
    event = get_object_or_404(Event, pk=e_id)
    return render(request, 'event_detail.html', {'event': event})


def participate(request, e_id):
    event = get_object_or_404(Event, pk=e_id)
    if request.method == 'POST':
        eventname = request.POST['eventname']
        eventdate = request.POST['eventdate']
        eventtime = request.POST['eventtime']
        email = request.POST['email']
        phone = request.POST['phone']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        location = request.POST['loaction']

        existing_participants = EventRequest.objects.filter(email=email)
        if existing_participants.exists():
            messages.error(request, 'You have already registered for this event.')
            return redirect('participate', e_id=event.e_id)

        new_event_request = EventRequest(
            eventname=eventname,
            eventdate=eventdate,
            eventtime=eventtime,
            email=email,
            phone=phone,
            firstname=firstname,
            lastname=lastname,
            location=location
        )

        new_event_request.save()
        messages.error(request, 'Thank you for participating. We will send you a confirmation email soon.')

        # Welcoming Email to Event Participants
        subject = "Welcome to the UIUPC Event"
        message = f"Dear {firstname} {lastname},\n\nWelcome to the UIUPC event! We are thrilled that you've decided to participate.\n\nEvent Details:\nEvent Name: {eventname}\nDate: {eventdate}\nTime: {eventtime}\n\nWe can't wait to see you at the event. Your participation is highly appreciated, and we're looking forward to a great experience together.\n\nIf you have any questions or need further information before the event, please don't hesitate to reach out to us.\n\nBest regards,\nTeam UIUPC"

        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        send_mail(subject, message, from_email, to_email, fail_silently=True)
        return redirect('participate', e_id)

    else:
        event = get_object_or_404(Event, pk=e_id)
        return render(request, 'participate.html', {'event': event})
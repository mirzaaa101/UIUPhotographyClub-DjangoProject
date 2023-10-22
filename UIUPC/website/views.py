from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RegistrationRequest
from UIUPC import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'home.html', {})


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
from django.contrib import admin
from .models import RegistrationRequest
from .models import Notice
from .models import FAQ
from .models import Event
from .models import EventRequest
from .models import About

# Register your models here.
admin.site.register(RegistrationRequest)
admin.site.register(Notice)
admin.site.register(FAQ)
admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(About)

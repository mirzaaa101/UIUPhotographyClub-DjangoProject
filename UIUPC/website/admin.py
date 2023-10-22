from django.contrib import admin
from .models import RegistrationRequest
from .models import Notice
from .models import FAQ

# Register your models here.
admin.site.register(RegistrationRequest)
admin.site.register(Notice)
admin.site.register(FAQ)

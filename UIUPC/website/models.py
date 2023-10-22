from django.db import models

class RegistrationRequest(models.Model):
    requested_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, unique=True)
    idnumber = models.CharField(max_length=10)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    dob = models.DateField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        if self.is_accepted == False:
            return f"Request From-{self.firstname} {self.lastname}"
        else:
            return f"You Accepted-{self.firstname} {self.lastname}'s Request"

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


class Notice(models.Model):
    n_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notice_title = models.CharField(max_length=200)
    notice_description = models.CharField(max_length=1000)
    notice_image = models.ImageField(upload_to='Files/Notice/')

    def __str__(self):
        return self.notice_title


class FAQ(models.Model):
    f_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.question}"


class Event(models.Model):
    e_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1200)
    location = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_photo = models.ImageField(upload_to='Files/Events/')
    join_event = models.BooleanField(default=False)

    def __str__(self):
        return f"Event-: {self.title}"

class EventRequest(models.Model):
    p_id = models.AutoField(primary_key=True)
    participated_at = models.DateTimeField(auto_now_add=True)
    eventname = models.CharField(max_length=200)
    eventdate = models.DateField()
    eventtime = models.TimeField()
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=11)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Participant Name-: {self.firstname} {self.lastname}"
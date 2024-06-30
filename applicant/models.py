from django.db import models
from users.models import User
from agency.models import Agency
from officer.models import OfficerInCharge
from status.models import Status

class ApplicantComplaint(models.Model):
    facebook_link = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    employer = models.CharField(max_length=255, blank=True, null=True)
    fra = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    contact1 = models.CharField(max_length=255, blank=True, null=True)
    contact2 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    relative_name = models.CharField(max_length=255, blank=True, null=True)
    relative_contact = models.CharField(max_length=255, blank=True, null=True)
    relative_relation = models.CharField(max_length=255, blank=True, null=True)
    officer_in_charge = models.ForeignKey(OfficerInCharge, on_delete=models.SET_NULL, null=True)
    last_remarks = models.TextField(blank=True, null=True)
    attachment = models.CharField(max_length=255, blank=True, null=True) # For docs, image, pdf, etc.
    arrival_date = models.DateTimeField(blank=True, null=True)
    arrival_remarks = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    last_update = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_notify = models.DateField(blank=True, null=True)
    chat_message_notify = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ApplicantRemarksHistory(models.Model):
    applicant_complaint = models.ForeignKey(ApplicantComplaint, related_name='remarks_history', on_delete=models.CASCADE)
    remarks = models.TextField()
    attachment = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.remarks[:50]

class ApplicantChat(models.Model):
    applicant = models.ForeignKey(ApplicantComplaint, related_name='chats', on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

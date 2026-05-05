from django.db import models

class Appointment(models.Model):
    customer_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=200, blank=True)
    preferred_date = models.CharField(max_length=100, blank=True)
    preferred_time = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.customer_name} – {self.preferred_date} ({self.city})"

    class Meta:
        ordering = ['-created_at']


class ChatSession(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    messages = models.JSONField(default=list)
    appointment = models.ForeignKey(Appointment, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_key}"

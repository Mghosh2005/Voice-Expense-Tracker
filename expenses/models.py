import uuid
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)
    event_ts = models.DateTimeField(default=timezone.now)
    amount_minor = models.IntegerField()
    currency = models.CharField(max_length=10, default="INR")
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, default="Other")
    convo_id = models.CharField(max_length=100, default="")
    source = models.CharField(max_length=50, default="voice")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id}: {self.description} ₹{self.amount_minor/100:.2f}"

class MonthlyRollup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)
    year_month = models.CharField(max_length=6)
    totals_by_category = models.JSONField(default=dict)
    total_amount_minor = models.IntegerField(default=0)
    top_items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


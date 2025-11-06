
import re
from .models import Transaction
from datetime import datetime

def parse_sms_text(text, user_id="demo_user"):
    text = text.lower()
    match = re.search(r'paid\s₹?(\d+)\s*to\s([\w\s&]+)', text)
    if not match:
        return None
    amount = int(match.group(1)) * 100
    receiver = match.group(2).strip().title()
    return Transaction.objects.create(
        user_id=user_id,
        amount_minor=amount,
        currency="INR",
        description=receiver,
        category="Other",
        source="sms",
        event_ts=datetime.now(),
    )

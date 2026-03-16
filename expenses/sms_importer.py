import re
from datetime import datetime
from .models import Transaction


def parse_sms_text(text: str, user_id: str = "demo_user"):
    """
    Parse a UPI/bank SMS and save a Transaction.
    Handles patterns like:
      'You paid ₹500 to Swiggy via UPI'
      'Paid Rs.300 to John on GPay'
    """
    text_lower = text.lower()

    match = re.search(
        r'(?:paid|sent|debited)[^\d]*(?:₹|rs\.?\s*)?(\d+(?:\.\d+)?)'
        r'(?:\s*to\s+([\w\s&]+?))?(?:\s+(?:via|on|using|through)\s|$)',
        text_lower
    )
    if not match:
        return None

    amount_minor = int(float(match.group(1)) * 100)
    receiver = (match.group(2) or "Unknown").strip().title()

    return Transaction.objects.create(
        user_id=user_id,
        amount_minor=amount_minor,
        currency="INR",
        description=receiver,
        category="Transfer",
        source="sms",
        event_ts=datetime.now(),
    )

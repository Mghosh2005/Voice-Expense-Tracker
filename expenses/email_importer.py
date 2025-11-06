from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import re
from .models import Transaction
from datetime import datetime
import os

def import_gmail_transactions(user_id="demo_user"):
    creds = Credentials.from_authorized_user_file(
        os.getenv("GMAIL_TOKEN_PATH", "token.json")
    )
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", q="from:(googlepay) OR from:(paytm) 'You paid'").execute()
    messages = results.get("messages", [])
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        body = msg["snippet"]
        match = re.search(r'₹(\d+)\s*to\s([\w\s&]+)', body)
        if match:
            amount = int(match.group(1)) * 100
            receiver = match.group(2).title()
            Transaction.objects.get_or_create(
                user_id=user_id,
                amount_minor=amount,
                currency="INR",
                description=receiver,
                category="Other",
                source="gmail",
                event_ts=datetime.now(),
            )


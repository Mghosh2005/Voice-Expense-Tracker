import re
import os
from datetime import datetime
from .models import Transaction


def import_gmail_transactions(user_id: str = "demo_user"):
    """
    Import transactions from Gmail using Google OAuth2.
    Requires GMAIL_TOKEN_PATH set in .env pointing to a valid token.json.
    """
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("google-api-python-client not installed. Skipping Gmail import.")
        return

    token_path = os.getenv("GMAIL_TOKEN_PATH", "token.json")
    if not os.path.exists(token_path):
        print(f"Gmail token not found at {token_path}. Skipping.")
        return

    creds = Credentials.from_authorized_user_file(token_path)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        q="from:(googlepay OR paytm OR phonepe) 'You paid'"
    ).execute()

    messages = results.get("messages", [])
    created = 0

    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        body = msg.get("snippet", "")

        match = re.search(r'(?:₹|rs\.?\s*)(\d+(?:\.\d+)?)\s*(?:to|for)\s*([\w\s&]+)', body, re.IGNORECASE)
        if match:
            amount_minor = int(float(match.group(1)) * 100)
            receiver = match.group(2).strip().title()

            _, was_created = Transaction.objects.get_or_create(
                user_id=user_id,
                amount_minor=amount_minor,
                description=receiver,
                source="gmail",
                defaults={
                    "currency": "INR",
                    "category": "Transfer",
                    "event_ts": datetime.now(),
                },
            )
            if was_created:
                created += 1

    print(f"Gmail import: {created} new transactions.")

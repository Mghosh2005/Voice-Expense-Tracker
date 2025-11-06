import re
from dateparser import parse as parse_date
from datetime import datetime

CATEGORIES = {
    "Food": ["coffee", "dinner", "restaurant", "meal", "snack"],
    "Subscription": ["netflix", "spotify", "amazon", "membership"],
    "Travel": ["cab", "train", "flight", "uber"],
    "Groceries": ["vegetables", "milk", "bread"],
    "Health": ["medicine", "doctor", "gym"],
    "Utilities": ["wifi", "electricity", "water", "phone"],
    "Shopping": ["clothes", "shoes", "bag"],
    "Entertainment": ["movie", "concert"],
    "Education": ["book", "course"],
}

def parse_expense(text: str):
    text_lower = text.lower()
    amount_match = re.search(r'(\d+(?:\.\d+)?)(?:\s?(?:rs|rupees|₹|inr|k))?', text_lower)
    amount_minor = 0
    if amount_match:
        amt = amount_match.group(1)
        amount_minor = int(float(amt) * 100)

    description = re.sub(r'(\d+|₹|rs|rupees|inr|today|yesterday)', '', text_lower).strip()
    category = "Other"
    for cat, keys in CATEGORIES.items():
        if any(k in text_lower for k in keys):
            category = cat
            break

    date_obj = parse_date(text) or datetime.now()

    return {
        "amount_minor": amount_minor,
        "currency": "INR",
        "description": description,
        "category": category,
        "event_ts": date_obj,
        "convo_id": "auto_" + datetime.now().strftime("%s"),
    }


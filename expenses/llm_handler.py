import re
from datetime import datetime

try:
    import dateparser
    HAS_DATEPARSER = True
except ImportError:
    HAS_DATEPARSER = False

# ─── Category keyword map ─────────────────────────────────────────────────────
CATEGORIES = {
    "Food":          ["coffee", "dinner", "lunch", "breakfast", "restaurant", "meal",
                      "snack", "tea", "food", "swiggy", "zomato", "pizza", "biryani",
                      "hotel", "cafe", "chai", "juice"],
    "Subscription":  ["netflix", "spotify", "amazon prime", "hotstar", "prime",
                      "membership", "subscription", "youtube"],
    "Travel":        ["cab", "train", "flight", "uber", "ola", "auto", "bus",
                      "metro", "rickshaw", "petrol", "diesel", "fuel", "toll"],
    "Groceries":     ["vegetables", "milk", "bread", "grocery", "groceries",
                      "rice", "dal", "atta", "oil", "sugar", "salt", "eggs"],
    "Health":        ["medicine", "doctor", "gym", "hospital", "pharmacy",
                      "clinic", "tablet", "medical", "health"],
    "Utilities":     ["wifi", "electricity", "water", "phone", "mobile",
                      "internet", "recharge", "bill", "gas"],
    "Shopping":      ["clothes", "shoes", "bag", "shirt", "dress", "amazon",
                      "flipkart", "online", "shop", "mall"],
    "Entertainment": ["movie", "concert", "game", "park", "event", "ticket"],
    "Education":     ["book", "course", "tuition", "school", "college", "fees"],
    "Transfer":      ["transfer", "sent", "upi", "neft", "rtgs", "payment"],
}


def detect_category(text: str) -> str:
    text_lower = text.lower()
    for cat, keywords in CATEGORIES.items():
        if any(k in text_lower for k in keywords):
            return cat
    return "Other"


def parse_amount(text: str) -> int:
    """Return amount in minor units (paise). Handles ₹500, Rs 500, 500k, 1.5k etc."""
    text_lower = text.lower()
    # Match patterns like ₹500, Rs500, 500 rupees, 1.5k
    pattern = r'(?:₹|rs\.?\s*|rupees?\s*)(\d+(?:\.\d+)?)(?:\s*k)?|(\d+(?:\.\d+)?)(?:\s*k)?\s*(?:₹|rs\.?|rupees?)'
    match = re.search(pattern, text_lower)
    if not match:
        # fallback: first standalone number
        match = re.search(r'\b(\d+(?:\.\d+)?)\b', text_lower)
        if not match:
            return 0
        amt_str = match.group(1)
        multiplier = 1000 if 'k' in text_lower[match.end():match.end()+2] else 1
    else:
        amt_str = match.group(1) or match.group(2) or "0"
        multiplier = 1000 if 'k' in text_lower[match.end():match.end()+2] else 1

    try:
        return int(float(amt_str) * multiplier * 100)
    except ValueError:
        return 0


def parse_date(text: str) -> datetime:
    if HAS_DATEPARSER:
        parsed = dateparser.parse(text, settings={"PREFER_DATES_FROM": "past"})
        if parsed:
            return parsed
    return datetime.now()


def clean_description(text: str) -> str:
    """Strip amounts, date words, and punctuation for a tidy description."""
    cleaned = re.sub(
        r'(?:₹|rs\.?\s*|rupees?\s*)\d+(?:\.\d+)?(?:\s*k)?'
        r'|\d+(?:\.\d+)?\s*(?:k\s*)?(?:₹|rs\.?|rupees?)?'
        r'|\b(?:today|yesterday|last\s+\w+|this\s+\w+|spent|paid|bought|for|on|at|the|i|a)\b',
        '', text, flags=re.IGNORECASE
    ).strip()
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip(' ,.-')
    return cleaned or text.strip()


def parse_expense(text: str) -> dict:
    """
    Parse a natural-language expense string.
    Returns a dict ready to feed into TransactionSerializer.
    """
    amount_minor = parse_amount(text)
    category = detect_category(text)
    description = clean_description(text)
    date_obj = parse_date(text)

    return {
        "amount_minor": amount_minor,
        "currency": "INR",
        "description": description,
        "category": category,
        "event_ts": date_obj,
        "convo_id": "auto_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "source": "web",
    }

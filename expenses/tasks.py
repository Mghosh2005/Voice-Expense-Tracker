from datetime import datetime
from django.db.models import Sum
from .models import Transaction, MonthlyRollup


def generate_monthly_rollup(user_id: str, year: int = None, month: int = None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    ym = f"{year}{month:02d}"

    txs = Transaction.objects.filter(
        user_id=user_id,
        event_ts__year=year,
        event_ts__month=month,
    )

    totals: dict = {}
    for t in txs:
        totals[t.category] = totals.get(t.category, 0) + t.amount_minor

    top_items = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:5]

    MonthlyRollup.objects.update_or_create(
        user_id=user_id,
        year_month=ym,
        defaults={
            "totals_by_category": totals,
            "total_amount_minor": sum(totals.values()),
            "top_items": top_items,
        },
    )

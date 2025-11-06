from datetime import datetime
from django.db.models import Sum
from .models import Transaction, MonthlyRollup

def generate_monthly_rollup(user_id):
    now = datetime.now()
    ym = now.strftime("%Y%m")
    txs = Transaction.objects.filter(user_id=user_id, event_ts__year=now.year, event_ts__month=now.month)
    totals = {}
    for t in txs:
        totals[t.category] = totals.get(t.category, 0) + t.amount_minor
    MonthlyRollup.objects.update_or_create(
        user_id=user_id,
        year_month=ym,
        defaults={
            "totals_by_category": totals,
            "total_amount_minor": sum(totals.values()),
            "top_items": sorted(totals.items(), key=lambda x: x[1], reverse=True)[:3],
        },
    )


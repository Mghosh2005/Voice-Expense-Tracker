from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Sum
from .models import Transaction, MonthlyRollup
from .serializers import TransactionSerializer, MonthlyRollupSerializer
from .llm_handler import parse_expense

@api_view(["POST"])
def log_expense(request):
    text = request.data.get("text")
    user_id = request.data.get("user_id", "demo_user")
    parsed = parse_expense(text)
    parsed["user_id"] = user_id
    parsed["source"] = "voice"
    serializer = TransactionSerializer(data=parsed)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def summary(request):
    user_id = request.GET.get("user_id", "demo_user")
    year_month = request.GET.get("year_month", datetime.now().strftime("%Y%m"))
    txs = Transaction.objects.filter(user_id=user_id, event_ts__startswith=year_month[:4])
    total = txs.aggregate(Sum("amount_minor"))["amount_minor__sum"] or 0
    data = {
        "user_id": user_id,
        "year_month": year_month,
        "total_minor": total,
        "totals_by_category": {
            cat: sum(t.amount_minor for t in txs.filter(category=cat))
            for cat in txs.values_list("category", flat=True).distinct()
        },
    }
    return Response(data)


from datetime import datetime
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction, MonthlyRollup
from .serializers import TransactionSerializer, MonthlyRollupSerializer
from .llm_handler import parse_expense
from .tasks import generate_monthly_rollup


@api_view(["POST"])
def parse_only(request):
    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "text field is required."}, status=status.HTTP_400_BAD_REQUEST)
    parsed = parse_expense(text)
    parsed["event_ts"] = parsed["event_ts"].isoformat()
    return Response(parsed, status=status.HTTP_200_OK)


@api_view(["POST"])
def log_expense(request):
    user_id = request.data.get("user_id", "demo_user")

    if "amount_minor" in request.data:
        parsed = {
            "user_id":      user_id,
            "amount_minor": request.data.get("amount_minor", 0),
            "currency":     request.data.get("currency", "INR"),
            "description":  request.data.get("description", ""),
            "category":     request.data.get("category", "Other"),
            "event_ts":     request.data.get("event_ts", datetime.now().isoformat()),
            "convo_id":     request.data.get("convo_id", ""),
            "source":       request.data.get("source", "voice"),
        }
    else:
        text = request.data.get("text", "").strip()
        if not text:
            return Response({"error": "Provide 'text' or a pre-parsed expense."}, status=status.HTTP_400_BAD_REQUEST)
        parsed = parse_expense(text)
        parsed["user_id"] = user_id
        parsed["source"]  = "web"

    serializer = TransactionSerializer(data=parsed)
    if serializer.is_valid():
        serializer.save()
        try:
            generate_monthly_rollup(user_id)
        except Exception:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_transactions(request):
    user_id    = request.GET.get("user_id", "demo_user")
    year_month = request.GET.get("year_month", datetime.now().strftime("%Y%m"))
    year  = int(year_month[:4])
    month = int(year_month[4:6])
    txs = Transaction.objects.filter(
        user_id=user_id,
        event_ts__year=year,
        event_ts__month=month,
    )
    return Response(TransactionSerializer(txs, many=True).data)


@api_view(["DELETE"])
def delete_transaction(request, pk):
    try:
        tx = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    tx.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def summary(request):
    user_id    = request.GET.get("user_id", "demo_user")
    year_month = request.GET.get("year_month", datetime.now().strftime("%Y%m"))
    year  = int(year_month[:4])
    month = int(year_month[4:6])
    txs   = Transaction.objects.filter(
        user_id=user_id,
        event_ts__year=year,
        event_ts__month=month,
    )
    total = txs.aggregate(Sum("amount_minor"))["amount_minor__sum"] or 0
    categories = txs.values_list("category", flat=True).distinct()
    totals_by_category = {
        cat: txs.filter(category=cat).aggregate(Sum("amount_minor"))["amount_minor__sum"] or 0
        for cat in categories
    }
    return Response({
        "user_id":                  user_id,
        "year_month":               year_month,
        "total_minor":              total,
        "total":                    total / 100,
        "totals_by_category":       totals_by_category,
        "totals_by_category_rupees":{k: v / 100 for k, v in totals_by_category.items()},
        "transaction_count":        txs.count(),
        "recent_transactions":      TransactionSerializer(txs[:5], many=True).data,
    })


@api_view(["GET"])
def all_time_summary(request):
    user_id = request.GET.get("user_id", "demo_user")
    txs     = Transaction.objects.filter(user_id=user_id)
    total   = txs.aggregate(Sum("amount_minor"))["amount_minor__sum"] or 0
    return Response({
        "user_id":           user_id,
        "total_minor":       total,
        "total":             total / 100,
        "transaction_count": txs.count(),
    })
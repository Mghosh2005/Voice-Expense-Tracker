from django.urls import path
from . import views

urlpatterns = [
    path("parse/", views.parse_only),                       # STT → parse (no save)
    path("log/", views.log_expense),                        # save confirmed expense
    path("transactions/", views.list_transactions),
    path("transactions/<str:pk>/", views.delete_transaction),
    path("summary/", views.summary),
    path("all-time-summary/", views.all_time_summary),
]

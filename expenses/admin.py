from django.contrib import admin
from .models import Transaction, MonthlyRollup


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'description', 'category', 'amount_display', 'source', 'event_ts')
    list_filter = ('category', 'source', 'currency')
    search_fields = ('user_id', 'description')
    ordering = ('-event_ts',)

    def amount_display(self, obj):
        return f"₹{obj.amount_minor / 100:.2f}"
    amount_display.short_description = 'Amount'


@admin.register(MonthlyRollup)
class MonthlyRollupAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'year_month', 'total_display', 'updated_at')
    ordering = ('-year_month',)

    def total_display(self, obj):
        return f"₹{obj.total_amount_minor / 100:.2f}"
    total_display.short_description = 'Total'

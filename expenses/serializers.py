from rest_framework import serializers
from .models import Transaction, MonthlyRollup

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class MonthlyRollupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyRollup
        fields = '__all__'


from rest_framework import serializers
from .models import Transaction, MonthlyRollup


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()   # expose the computed property

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class MonthlyRollupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyRollup
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

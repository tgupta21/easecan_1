from rest_framework import serializers
from .models import Refund
from transaction.models import Transaction


class RefundSerializer(serializers.ModelSerializer):
    """Serialize the refund object"""
    id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Refund
        fields = ('id', 'currency', 'amount', 'reference_id', 'time')
        read_only_fields = ('reference_id', 'time')

    def create(self, validated_data):
        transaction_id = validated_data.pop('id')
        response = validated_data.pop('response')
        reference_id = response.get('reference_id')
        refund = Refund(**validated_data, reference_id=reference_id)
        refund.save()
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.refund_detail = refund
        transaction.save()
        return refund

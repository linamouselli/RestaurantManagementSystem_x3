from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','first_name','last_name','email','phone','address','registration_date']
        read_only_fields = ['registration_date']

    def validate(self, data):

        customer = Customer(**data)

        try:
            customer.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)

        return data

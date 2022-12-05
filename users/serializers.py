from rest_framework import serializers

from .models import *

class CouponsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = ['coupon_code', 'valid_num_of_use', 'percent',]


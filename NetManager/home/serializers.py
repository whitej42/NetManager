from rest_framework import serializers

from device.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'name',
            'type',
            'host',
            'vendor',
            'location',
            'contact',
        ]

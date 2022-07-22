from rest_framework import serializers
from .models import WaterTank, WaterLevel


class TankSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if(self.context.get('view').action == 'retrieve'):
            self.fields['levels'] = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = WaterTank
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'required': False},
        }


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaterLevel
        fields = '__all__'
        read_only_fields = ('id',)

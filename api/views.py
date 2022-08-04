from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import WaterLevel, WaterTank
from rest_framework.response import Response
from .serializers import TankSerializer, LevelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class WaterTankView(ModelViewSet):
    serializer_class = TankSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WaterTank.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer: TankSerializer):
        serializer.save(user=self.request.user)


class WaterLevelView(APIView):
    serializer_class = LevelSerializer

    def post(self, request, tank_id):
        tank = WaterTank.objects.get(id=tank_id)
        if not tank:
            raise ValidationError('Tank not found')
        level = LevelSerializer(
            data=request.data)
        if(level.is_valid()):
            level.save(water_tank=tank)
            return Response(level.data)
        return Response(level.errors, status=400)

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
User = settings.AUTH_USER_MODEL


class WaterTank(models.Model):

    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, related_name='water_tanks', on_delete=models.CASCADE)
    capacity = models.IntegerField()
    depth = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class WaterLevel(models.Model):

    water_tank = models.ForeignKey(
        WaterTank, related_name="levels", on_delete=models.CASCADE)
    level = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.water_tank.name + " " + str(self.level)


@receiver(post_save, sender=WaterLevel)
def update_tank_level(sender, instance, created, **kwargs):
    if created:
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'tank_{}'.format(instance.water_tank.id),
            {
                "type": "level_update",
                "message": instance.level
            })

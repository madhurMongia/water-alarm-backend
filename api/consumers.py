import json
from channels.generic.websocket import WebsocketConsumer
from .models import WaterLevel, WaterTank
from asgiref.sync import async_to_sync


class CurrentLevelConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        tank_id = self.scope['url_route']['kwargs']['pk']
        async_to_sync(self.channel_layer.group_add)(group='tank_{}'.format(
            tank_id), channel=self.channel_name)
        self.set_tank(tank_id)
        self.send(text_data=json.dumps({
            'message': 'Connected successfully with {}'.format(self.tank.name)
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        if(type == 'current_level'):
            self.get_current_level()

    def set_tank(self, tank_id):
        self.tank = WaterTank.objects.get(id=tank_id)

    def get_current_level(self):
        level = WaterLevel.objects.filter(
            water_tank=self.tank).order_by('-created_at').first()
        if(level):
            self.send(text_data=json.dumps({
                'message': level.level
            }))
        else:
            self.send(text_data=json.dumps({
                'message': 'No level data'
            }))

    def level_update(self, event):
        self.send(text_data=json.dumps({
            'message': 'Current level is {}'.format(event['message'])
        }))

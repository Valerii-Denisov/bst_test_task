from robots.models import Robot
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class RobotsFactory(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        robot_model = str(data.get('model'))
        robot_version = str(data.get('version'))
        robot_serial = '{0}-{1}'.format(robot_model, robot_version)
        robot_created = data.get('created')
        robot_data = {
            'serial': robot_serial.lower(),
            'model': robot_model.lower(),
            'version': robot_version.lower(),
            'created': robot_created,
        }
        robot_item = Robot.objects.create(**robot_data)
        data = {
                "message": f"New robot added to "
                           f"warehouse with id: {robot_item.id}"
        }
        return JsonResponse(data, status=201)

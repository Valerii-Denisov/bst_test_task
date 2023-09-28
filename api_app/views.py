import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot


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
        message = 'New robot added to warehouse with id: {0}'.format(
            robot_item.id,
        )
        response_data = {"message": message}
        return JsonResponse(response_data, status=201)

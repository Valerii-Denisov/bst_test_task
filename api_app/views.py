from django.shortcuts import render
from robots.models import Robot
from robots.validator import validate_robot_data
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class RobotsFactory(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        robot_serial = data.get('serial')
        robot_model = data.get('model')
        robot_version = data.get('version')
        robot_created = data.get('created')
        robot_data = {
            'serial': robot_serial,
            'model': robot_model,
            'version': robot_version,
            'created': robot_created,
        }
        with open('robots/models_list.json') as json_file:
            models_list = json.load(json_file)
        if validate_robot_data(robot_data, models_list.get('robot_models')):
            robot_item = Robot.objects.create(**robot_data)
            data = {
                "message": f"New robot added to "
                           f"warehouse with id: {robot_item.id}"
            }
            return JsonResponse(data, status=201)
# Create your views here.

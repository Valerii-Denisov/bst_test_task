import json
import os

from django.core.exceptions import ValidationError

from R4C.settings import BASE_DIR


def validate_robot_data(value):
    with open(os.path.join(BASE_DIR, 'models_list.json')) as json_file:
        models_list = json.load(json_file)
    if value not in models_list.get('robot_models'):
        raise ValidationError(
            'The {0} robot model is not '
            'manufactured at this factory'.format(value)
        )

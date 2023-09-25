from django.core.exceptions import ValidationError


def validate_robot_data(robot_data, models_list):
    robot_model = robot_data.get('model')
    if robot_model not in models_list:
        raise ValidationError(
            'The {0} robot model is not '
            'manufactured at this factory'.format(robot_model)
        )
    return True
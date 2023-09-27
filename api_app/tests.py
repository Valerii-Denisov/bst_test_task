from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from robots.models import Robot
import json


class ApiTestCase(TestCase):
    def setUp(self):
        self.create_robot = reverse('robot_create')
        self.get_report = reverse('report')
        self.valid_data = {
            'model': 'R2',
            'version': 'D2',
            'created': '2022-09-27 23:59:59'
        }
        self.invalid_data = {
            'model': 'T',
            'version': '01',
            'created': '2099-09-27 23:59:59'
        }

    def test_valid_robot_create(self):
        request = self.client.post(
            self.create_robot,
            json.dumps(self.valid_data),
            follow=True,
            content_type="application/json"
        )
        self.assertTrue(Robot.objects.get(pk=1))
        self.assertContains(
            request,
            'New robot added to warehouse with id: 1'.format(self),
            status_code=201
        )

    def test_invalid_robot_create(self):
        with self.assertRaises(ValidationError) as e:
            request = self.client.post(
                self.create_robot,
                json.dumps(self.invalid_data),
                follow=True,
                content_type="application/json"
            )

    def test_generate_report(self):
        response = self.client.get(self.get_report)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename={date}-factory_report.xlsx'.format(
                date=datetime.now().strftime('%Y-%m-%d')))

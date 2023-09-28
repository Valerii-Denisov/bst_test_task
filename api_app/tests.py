import json

from datetime import datetime

from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from robots.models import Robot
from django.core.exceptions import ValidationError
from customers.models import Customer
from orders.models import Order
from .models import OrdersQueue


class ApiTestCase(TestCase):
    fixtures = ['customers.json']

    def setUp(self):
        self.customer = Customer.objects.get(pk=1)
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
            'New robot added to warehouse with id: 1',
            status_code=201
        )

    def test_invalid_robot_create(self):
        with self.assertRaises(ValidationError):
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

    def test_signals_and_sending_email(self):
        order_data = {
            'customer': self.customer,
            'robot_serial': 'r2-d2',
        }
        order = Order.objects.create(**order_data)
        self.assertEqual(len(OrdersQueue.objects.all()), 1)
        robot_data = {
            'serial': 'r2-d2',
            'model': 'r2',
            'version': 'd2',
            'created': '2022-09-27 23:59:59',
        }
        robot = Robot.objects.create(**robot_data)
        self.assertEqual(OrdersQueue.objects.get(pk=1).status, 'Done')
        self.assertEqual(len(mail.outbox), 1)
        _mail = mail.outbox[0]
        self.assertIn(self.customer.email, _mail.to)
        message = render_to_string('email_text.html', {
            'model': robot_data.get('model').upper(),
            'version': robot_data.get('version').upper()
        })
        self.assertEqual(_mail.body, message)

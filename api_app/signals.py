from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from orders.models import Order
from robots.models import Robot
from .models import OrdersQueue
from .utils import send_email


@receiver(post_save, sender=Order)
def check_robot_in_warehouse(sender, instance, created, **kwargs):
    if created:
        serial = instance.robot_serial
        robots_in_warehouse = Robot.objects.filter(
            serial=serial,
        ).count()
        order_of_robot = Order.objects.filter(robot_serial=serial).count()
        if order_of_robot > robots_in_warehouse:
            OrdersQueue.objects.create(order=instance)


@receiver(post_save, sender=Robot)
def check_order_to_this_robot(sender, instance, created, **kwargs):
    if created:
        robot_serial = instance.serial
        orders_queue = OrdersQueue.objects.select_related('order').filter(
            order__robot_serial=robot_serial, status='Wait'
        ).order_by('id')
        if len(orders_queue) > 0:
            order = orders_queue[0]
            order.status = 'Done'
            order.save()


@receiver(post_save, sender=OrdersQueue)
def send_email_to_customer(sender, instance, created, **kwargs):
    if not created:
        robot_data = instance.order.robot_serial.split('-')
        mail_subject = 'Робот появился на складе'
        message = render_to_string('email_text.html', {
            'model': robot_data[0].upper(),
            'version': robot_data[1].upper()
        })
        to_email = instance.order.customer.email
        send_email(mail_subject, message, to_email)

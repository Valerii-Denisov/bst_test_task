from django.db import models
from orders.models import Order

# Create your models here.
class OrdersQueue(models.Model):
    STATUS_OF_ORDER = [
        ('Done', 'Order is done'),
        ('Wait', 'Customer is waiting his robot'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=4,
        choices=STATUS_OF_ORDER,
        default='Wait',
    )

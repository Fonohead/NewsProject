from email.policy import default
from random import choices

from django.db import models
from datetime import datetime

from .resources import POSITIONS

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default='DI')
    labour_contract = models.IntegerField()

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default='Состав не указан')

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_order_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def order_summ(self):
        return self.product.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()





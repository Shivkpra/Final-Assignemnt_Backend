from django.utils import timezone
from django.db import models

# created model in which data of success will stored


class Payment_placed(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    amount_paid = models.IntegerField()
    py_mode = models.CharField(max_length=200, blank=False, null=False)
    order_time = models.DateTimeField(default=timezone.now, blank=True)


"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customer_profile (sender,instance,create, **kwargs):
    if create:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.username,email=instance.email)


post_save.connect(customer_profile,sender=User)

"""
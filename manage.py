#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()
from django.contrib.auth.models import User
from django.utils import timezone
from project.models import Customer, Order
from uuid import uuid4

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def createsuperuser():
    user = User.objects.create_superuser(
        username='admin',
        password='admin',
        email='test@ecommerce.com',
        last_login=timezone.now()
    )
    customer = Customer.objects.create(
                user=user,
                name=user.first_name,
                email=user.email,
                auth_token=str(uuid4()),
                is_verified=True
            )
    order = Order.objects.create(
        customer=customer,
        order_type='cart_order'
    )
    customer.save()
    order.save()

if __name__ == '__main__':
    if sys.argv[1] == 'createsuperuser':
        createsuperuser()
        exit()
    main()

from django.dispatch import Signal

__all__ = ['user_registered']

user_registered = Signal(providing_args=[
    'user', 'request', 'customer', 'last4', 'plan',
])

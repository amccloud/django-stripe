from django.conf import settings

STRIPE_PRIVATE_KEY = getattr(settings, 'STRIPE_PRIVATE_KEY')
STRIPE_PUBLIC_KEY = getattr(settings, 'STRIPE_PUBLIC_KEY')
STRIPE_VALIDATE_CARD = getattr(settings, 'STRIPE_VALIDATE_CARD', True)
STRIPE_WEBHOOK_ENDPOINT = getattr(settings, 'STRIPE_WEBHOOK_ENDPOINT')
STRIPE_PLAN_CHOICES = getattr(settings, 'STRIPE_PLAN_CHOICES', ())

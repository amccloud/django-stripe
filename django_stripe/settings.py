from django.conf import settings

STRIPE_SECRET_KEY = getattr(settings,
    'STRIPE_SECRET_KEY'
)

STRIPE_PUBLISHABLE_KEY = getattr(settings,
    'STRIPE_PUBLISHABLE_KEY'
)

STRIPE_WEBHOOK_SECRET = getattr(settings,
    'STRIPE_WEBHOOK_SECRET'
)

STRIPE_WEBHOOK_ENDPOINT = getattr(settings,
    'STRIPE_WEBHOOK_ENDPOINT', r'stripe/%s/webhook/' % STRIPE_WEBHOOK_SECRET
)

STRIPE_PLAN_CHOICES = getattr(settings,
    'STRIPE_PLAN_CHOICES', ()
)

STRIPE_CUSTOMER_DESCRIPTION = getattr(settings,
    'STRIPE_CUSTOMER_DESCRIPTION', lambda u: str(u)
)

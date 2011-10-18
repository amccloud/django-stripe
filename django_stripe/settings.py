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

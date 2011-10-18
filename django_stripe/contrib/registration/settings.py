from django.conf import settings

SUBSCRIPTION_PLAN_CHOICES = getattr(settings,
    'SUBSCRIPTION_PLAN_CHOICES'
)

SUBSCRIPTION_CUSTOMER_DESCRIPTION = getattr(settings,
    'SUBSCRIPTION_CUSTOMER_DESCRIPTION', lambda u: str(u)
)

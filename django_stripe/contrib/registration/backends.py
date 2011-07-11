from django.contrib.auth.models import Group
from registration.backends.simple import SimpleBackend

class StripeSubscriptionBackend(SimpleBackend):
    def register(self, request, plan, **kwargs):
        group = Group.objects.get(pk=plan)
        new_user = super(StripeSubscriptionBackend, self).register(request, **kwargs)
        new_user.groups.add(group)
        return new_user

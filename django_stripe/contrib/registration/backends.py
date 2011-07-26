from django.contrib.auth.models import Group
from django.utils.functional import curry
from registration.backends.simple import SimpleBackend
from .forms import CreditCardRegistrationForm

class StripeSubscriptionBackend(SimpleBackend):
    def get_form_class(self, request):
        return curry(CreditCardRegistrationForm, initial={
            'plan': request.GET.get('plan'),
        })

    def register(self, request, plan, **kwargs):
        new_user = super(StripeSubscriptionBackend, self).register(request, **kwargs)
        try:
            group = Group.objects.get(pk=plan)
            new_user.groups.add(group)
        except Group.DoesNotExist:
            pass
        return new_user

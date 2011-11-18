from django.contrib.auth.decorators import login_required

from django_stripe.views import BaseCardTokenFormView

class AccountBillingFormView(BaseCardTokenFormView):
    def get_last4(self):
        user_profile = self.request.user.get_profile()

        return user_profile.card_last4

    def form_valid(self, form):
        customer = form.save(self.request.user)

        user_profile = self.request.user.get_profile()
        user_profile.customer_id = customer.id
        user_profile.card_last4 = customer.active_card.last4
        user_profile.save()

        return super(AccountBillingFormView, self).form_valid(form)

account_billing_form = login_required(AccountBillingFormView.as_view())

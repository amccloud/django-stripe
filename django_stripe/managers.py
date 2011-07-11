from django.db import models
from stripe import StripeError

class SwipeResourceManager(models.Manager):
    def create(self, **kwargs):
        try:
            self.model.resource.create(**kwargs)
            return super(SwipeResourceManager, self).create(**kwargs)
        except StripeError:
            raise

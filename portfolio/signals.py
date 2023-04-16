"""
Signals are used in Django to notify other parts of the app when certain actions occur. In this case, the signals are
used to create a profile, save a profile, decrease the bank balance on Income object deletion, and increase the bank
balance on Expenses object deletion. All four signal are imported into the apps.py file.
"""
from django.contrib.auth.models import User  # associated built-in model
from .models import Profile, Income, Expenses  # associated models from models.py
from django.db.models.signals import post_save, post_delete  # different types of signals (by circumstances)
from django.dispatch import receiver  # receiver is a decorator (additional function)


# After creating a user, a profile is automatically created
@receiver(post_save, sender=User)  # if the User object is saved, the function under the decorator is initialized
def create_profile(sender, instance, created, **kwargs):  # 'instance' is the newly created User object
    if created:
        Profile.objects.create(user=instance)


# After update of user details, user profile will be also saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# After deleting of Income object, bank balance associated with the income line will be decreased by amount of
# income amount
@receiver(post_delete, sender=Income)
def decrease_bank_balance_on_delete(sender, instance, **kwargs):
    bank = instance.bank
    if bank:
        bank.balance -= instance.amount
        bank.save()


# After deleting of Expenses object, bank balance associated with the expenses line will be increased by amount of
# expenses amount
@receiver(post_delete, sender=Expenses)
def increase_bank_balance_on_delete(sender, instance, **kwargs):
    bank = instance.bank
    if bank:
        bank.balance += instance.amount
        bank.save()

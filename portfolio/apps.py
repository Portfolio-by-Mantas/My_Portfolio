"""
This is a configuration file for a Django app called 'portfolio'. The AppConfig class is used to configure an app's
settings, it is registered in the list of 'INSTALLED_APPS' at mysite/settings.py.

In this case, the default_auto_field is set to django.db.models.BigAutoField, which is a field that automatically
generates big integers for primary keys.
In Django, every model needs a primary key to uniquely identify each record in the database. By default, Django uses
an AutoField to create an integer-based primary key. However, for some use cases, the standard AutoField may not be
sufficient to store large numbers of records. This is where BigAutoField comes into play. A BigAutoField is similar to
AutoField, but it uses a 64-bit integer instead of a 32-bit integer. This means that it can handle much larger numbers
than the default AutoField, making it suitable for models with large amounts of data.

The ready() method is a method that is called when the app is ready to run. It is used to set up any necessary
configurations or connections. In this case, the ready() method imports four signals from the signals.py module of the
'portfolio' app. Read more about those at signals.py.
"""
from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    def ready(self):
        from .signals import create_profile, save_profile, decrease_bank_balance_on_delete, \
            increase_bank_balance_on_delete

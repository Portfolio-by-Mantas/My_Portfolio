from datetime import date
from django.core.exceptions import ValidationError


# Validation method for Income and Expenses models, date variable
def present_or_past_date(value):
    if value > date.today():
        raise ValidationError("The date entered cannot be greater than today's date.")
    return value

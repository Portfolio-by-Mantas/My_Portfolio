from django.contrib.auth.models import User  # associated built-in model
# associated models from models.py:
from .models import Profile, Income, Expenses, IncomeSource, IncomeCategory, ExpensesCategory, Seller, Bank
from django import forms  # provides a way to define HTML form elements in Python.


# Form used to update a user's information
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # The email field is overridden to use an EmailField instead of the default CharField.
# It provides validation that the email address is properly formatted and includes a valid domain name.
# Additionally, it is checking that the email address is unique within the database.

    class Meta:
        model = User
        fields = ['username', 'email']


# A form used to update a user's profile photo
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class DateInput(forms.DateInput):
    input_type = 'date'


"""
A custom DateInput class is defined that is a subclass of forms.DateInput. 
It is used to override the default input type for date fields in forms to use the HTML5 date input type instead of the 
default text type. This provides a more user-friendly interface for selecting dates.
"""

"""Below are forms to create essential objects for this program basic functionality:"""

""" It should be noted that almost in all the forms is used function 'def __init__'. 
__init__() is a special method in Python classes that gets called when an instance of the class is created.
In the context of these Django forms, method is used to customize the form by filtering the queryset of the fields based 
on the current user. In this case, the *args and **kwargs parameters are used to accept any additional arguments that 
might be passed to the form's constructor. These arguments are then passed to the parent class's constructor using 
super(). This allows the parent class (in this case, forms.ModelForm or forms.Form) to perform its own initialization 
tasks before the custom initialization code in the __init__() method is executed. """


# Form is designed to create Income instance, it is needed to fill fields described in Meta class
class IncomeCreateForm(forms.ModelForm):  # method is used to customize the form by selecting fields ...
    def __init__(self, user, *args, **kwargs):
        super(IncomeCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = IncomeCategory.objects.filter(client=user)  # ... based on the current user
        self.fields['source'].queryset = IncomeSource.objects.filter(earner=user)  # this means that user can only ...
        self.fields['bank'].queryset = Bank.objects.filter(owner=user)  # select those choices that created previously
        # The user argument is passed to the method and used to filter the objects based on the user's ID.

    class Meta:
        model = Income
        fields = ['date', 'amount', 'category', 'source', 'bank', 'notes', 'pdf']
        widgets = {'date': DateInput()}  # For date uses custom (previously described) DateInput class


# Form is designed to create Expenses instance, it is needed to fill fields described in Meta class
class ExpensesCreateForm(forms.ModelForm):  # method is used to customize the form by selecting fields ...
    def __init__(self, user, *args, **kwargs):
        super(ExpensesCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpensesCategory.objects.filter(client=user)  # ... based on the current user
        self.fields['seller'].queryset = Seller.objects.filter(client=user)  # this means that user can only ...
        self.fields['bank'].queryset = Bank.objects.filter(owner=user)  # select those choices that created previously
        # The user argument is passed to the method and used to filter the objects based on the user's ID.

    class Meta:
        model = Expenses
        fields = ['date', 'amount', 'category', 'seller', 'bank', 'notes', 'pdf']
        widgets = {'date': DateInput()}  # For date uses custom (previously described) DateInput class


class BankCreateForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'balance', 'investment']


class IncomeCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['definition']


class IncomeSourceCreateForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['source']


class ExpensesCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ExpensesCategory
        fields = ['definition']


class SellerCreateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['seller']


"""
Below are three forms for transfers between Bank 'accounts'. Two forms are intended for inside transfers (among bank's 
balance and investment) and one - between banks transfers. A total of eight forms are also provided for data retrieval.
"""


# First form intended for inside transfer, functional usage described at views_banks.py
class TransferInsideBankForm(forms.Form):
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), label='Select bank')  # A dropdown for selecting the bank
    source_account = forms.ChoiceField(choices=[('balance', 'Account'), ('investment', 'Investment')], label='From')
    to_account = forms.ChoiceField(choices=[('balance', 'Account'), ('investment', 'Investment')], label='Into')
    amount = forms.DecimalField(label='Transfer amount', max_digits=10, decimal_places=2)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering bank field ...
        super(TransferInsideBankForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = Bank.objects.filter(owner=user)  # ... based on the current user
        # The user argument is passed to the method and used to filter the banks based on the user's ID.


# A simpler form of internal transfer for use on a separate template, functional usage described at views_banks.py
class TransferInsideBankForDetailViewForm(forms.Form):
    #  The user enters the amount in the input of the account that he wants to top up:
    balance_to_investment = forms.DecimalField(label='Transfer from account to investment balance', decimal_places=2,
                                               max_digits=10, required=False)
    investment_to_balance = forms.DecimalField(label='Transfer from investment to account balance', decimal_places=2,
                                               max_digits=10, required=False)


# Form for transfer between banks, functional usage described at views_banks.py
class TransferBetweenBanksForm(forms.Form):
    # Two dropdowns for selecting the bank provider and the destination bank ant the transfer amount:
    from_bank = forms.ModelChoiceField(queryset=Bank.objects.all(), label='From bank')
    to_bank = forms.ModelChoiceField(queryset=Bank.objects.all(), label='Into bank')
    amount = forms.DecimalField(label='Transfer amount', max_digits=10, decimal_places=2)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering bank fields ...
        super(TransferBetweenBanksForm, self).__init__(*args, **kwargs)
        self.fields['from_bank'].queryset = Bank.objects.filter(owner=user)  # ... based on the current user
        self.fields['to_bank'].queryset = Bank.objects.filter(owner=user)
        # The user argument is passed to the method and used to filter the banks based on the user's ID.


# Form is designed to search for income objects by their variables, selecting them from the dropdowns (except dates)
class SearchSelectIncomeForm(forms.Form):  # required=False means that fields are not required to be filled out by user
    # There are no a required fields, meaning that the user can choose to leave any of them blank
    start_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), required=False)
    source = forms.ModelChoiceField(queryset=IncomeSource.objects.all(), required=False)
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(SearchSelectIncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = IncomeCategory.objects.filter(client=user)  # ... based on ...
        self.fields['source'].queryset = IncomeSource.objects.filter(earner=user)  # ... the current user
        self.fields['bank'].queryset = Bank.objects.filter(owner=user)
        # The user argument is passed to the method and used to filter the objects based on the user's ID.


# Mirror form (to previous) for comparing received income objects in the same template
class SearchSelectIncomeForComparisonForm(forms.Form):
    start_date_compare = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date_compare = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    category_compare = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), required=False)
    source_compare = forms.ModelChoiceField(queryset=IncomeSource.objects.all(), required=False)
    bank_compare = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):
        super(SearchSelectIncomeForComparisonForm, self).__init__(*args, **kwargs)
        self.fields['category_compare'].queryset = IncomeCategory.objects.filter(client=user)
        self.fields['source_compare'].queryset = IncomeSource.objects.filter(earner=user)
        self.fields['bank_compare'].queryset = Bank.objects.filter(owner=user)


# Form is designed to search for expenses objects by their variables, selecting them from the dropdowns (except dates)
class SearchSelectExpensesForm(forms.Form):
    # There are no a required fields, meaning that the user can choose to leave any of them blank
    start_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category = forms.ModelChoiceField(queryset=ExpensesCategory.objects.all(), required=False)
    source = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(SearchSelectExpensesForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpensesCategory.objects.filter(client=user)  # ... based on the current user
        self.fields['source'].queryset = Seller.objects.filter(client=user)
        self.fields['bank'].queryset = Bank.objects.filter(owner=user)
        # The user argument is passed to the method and used to filter the objects based on the user's ID.


# Mirror form (to previous) for comparing received expenses objects in the same template
class SearchSelectExpensesForComparisonForm(forms.Form):
    start_date_compare = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date_compare = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    category_compare = forms.ModelChoiceField(queryset=ExpensesCategory.objects.all(), required=False)
    source_compare = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)
    bank_compare = forms.ModelChoiceField(queryset=Bank.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):
        super(SearchSelectExpensesForComparisonForm, self).__init__(*args, **kwargs)
        self.fields['category_compare'].queryset = ExpensesCategory.objects.filter(client=user)
        self.fields['source_compare'].queryset = Seller.objects.filter(client=user)
        self.fields['bank_compare'].queryset = Bank.objects.filter(owner=user)


# Form is designed to filter out income objects for report, by date, source and category, selecting it from dropdown
class ArchiveIncomeForm(forms.Form):
    # All fields are not required, meaning that the user can choose to leave any of them blank
    start_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category = forms.ModelChoiceField(queryset=IncomeCategory.objects.none(), required=False)
    source = forms.ModelChoiceField(queryset=IncomeSource.objects.none(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(ArchiveIncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = IncomeCategory.objects.filter(client=user)  # ... based on the current user
        self.fields['source'].queryset = IncomeSource.objects.filter(earner=user)
        # The user argument is passed to the method and used to filter the objects based on the user's ID.


# Form is designed filter and display income data for a given month, allows user to select a date range for the report
class ArchiveIncomeByMonthForm(forms.Form):
    # All fields are not required, meaning that the user can choose to leave any of them blank
    start_date_report = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date_report = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category_report = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), required=False)
    source_report = forms.ModelChoiceField(queryset=IncomeSource.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(ArchiveIncomeByMonthForm, self).__init__(*args, **kwargs)
        self.fields['category_report'].queryset = IncomeCategory.objects.filter(client=user)  # ... based on ...
        self.fields['source_report'].queryset = IncomeSource.objects.filter(earner=user)  # ... the current user
        # The user argument is passed to the method and used to filter the objects based on the user's ID.


# Form is designed to filter out expenses objects for report, by date, source and category, selecting it from dropdown
class ArchiveExpensesForm(forms.Form):
    # All fields are not required, meaning that the user can choose to leave any of them blank
    start_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category = forms.ModelChoiceField(queryset=ExpensesCategory.objects.all(), required=False)
    source = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(ArchiveExpensesForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpensesCategory.objects.filter(client=user)  # ... based on ...
        self.fields['source'].queryset = Seller.objects.filter(client=user)  # ... the current user
        # The user argument is passed to the method and used to filter the objects based on the user's ID.


# Form is designed filter and display expenses data for a given month, allows user to select a date range for the report
class ArchiveExpensesByMonthForm(forms.Form):
    # All fields are not required, meaning that the user can choose to leave any of them blank
    start_date_report = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date_report = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    # Type attribute is set to date, which tells the browser to display a calendar picker for the user to select a date
    category_report = forms.ModelChoiceField(queryset=ExpensesCategory.objects.all(), required=False)
    source_report = forms.ModelChoiceField(queryset=Seller.objects.all(), required=False)

    def __init__(self, user, *args, **kwargs):  # method is used to customize the form by filtering fields ...
        super(ArchiveExpensesByMonthForm, self).__init__(*args, **kwargs)
        self.fields['category_report'].queryset = ExpensesCategory.objects.filter(client=user)  # ... based on ...
        self.fields['source_report'].queryset = Seller.objects.filter(client=user)  # ... the current user
        # The user argument is passed to the method and used to filter the objects based on the user's ID.

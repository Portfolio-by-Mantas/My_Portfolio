from django.shortcuts import render
from django.db.models import Sum
from django.template.defaultfilters import floatformat  # to format the floating-point number
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Bank
from .forms import BankCreateForm, TransferBetweenBanksForm, TransferInsideBankForm, TransferInsideBankForDetailViewForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.generic.edit import FormMixin  # is a class-based view mixin that provides methods and attributes to
# handle form processing and rendering. In the code it is intended to be used in conjunction with DetailView


# Displays the details of a single object and perform transfers between accounts within the same bank
class BankByUserDetailView(LoginRequiredMixin, FormMixin, DetailView):  # requires user to be logged-in to access view
    model = Bank
    context_object_name = 'banks'
    template_name = 'user_bank.html'
    form_class = TransferInsideBankForDetailViewForm

    def post(self, request, *args, **kwargs):  # Method is overridden to handle the form submission
        bank = self.get_object()
        form = self.get_form()
        # If the form is valid, the balance and investment amounts are transferred between accounts within the same bank
        if form.is_valid():
            balance_to_investment = form.cleaned_data['balance_to_investment']
            investment_to_balance = form.cleaned_data['investment_to_balance']
            if balance_to_investment:
                bank.balance -= balance_to_investment
                bank.investment += balance_to_investment
            if investment_to_balance:
                bank.investment -= investment_to_balance
                bank.balance += investment_to_balance
            bank.save()
            messages.success(request, 'Your funds have been transferred between the accounts!')
        return self.get(request, *args, **kwargs)  # is a call to the parent class's get method with the same arguments
    # used to re-render the view with any updated data that may have been modified as a result of the form submission


# Class-based view that is used to create a new Bank object for the logged-in user
class BankByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bank
    success_url = "/portfolio/bank/new"
    template_name = 'user_bank_form.html'
    form_class = BankCreateForm  # sets the form class that will be used to create the new object
    success_message = "Bank item was created successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.owner = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response


# Class-based view that is used to update an existing Bank object for the logged-in user
# TestMixin used to restrict access, the test function checks if the user meets criteria and can access the view
class BankByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Bank
    fields = ['name', 'balance', 'investment']
    success_url = "/portfolio/my_banks"
    template_name = 'user_bank_form.html'
    success_message = "Bank item was updated successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.owner = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response

    def test_func(self):  # checks whether the user requesting to update a Bank object is the owner of that object
        bank = self.get_object()
        return self.request.user == bank.owner
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# Class-based view that is used to delete an existing Bank object for the logged-in user
# TestMixin used to restrict access, the test function checks if the user meets criteria and can access the view
class BankByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Bank
    context_object_name = 'banks'
    success_url = "/portfolio/my_banks"
    template_name = 'user_bank_delete.html'
    success_message = "Bank item was deleted successfully."

    def test_func(self):  # checks whether the user requesting to delete a Bank object is the owner of that object
        bank = self.get_object()
        return self.request.user == bank.owner
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# Class-based view that is used to display an existing Bank objects for the logged-in user
class ListedBanksByUserListView(LoginRequiredMixin, ListView):
    model = Bank
    context_object_name = 'banks'
    template_name = 'user_banks.html'
    paginate_by = 10

    def get_queryset(self):  # overrides the default queryset to return only banks owned by the current user
        user = self.request.user
        return Bank.objects.filter(owner=user)

    # Calculates the total balance and investment of all the banks owned by the current user
    def get_context_data(self, **kwargs):  # used to add custom data that is needed for the template
        context = super().get_context_data(**kwargs)
        total_balance = self.get_queryset().aggregate(Sum('balance'))['balance__sum']  # First calculation
        # 1. Returns a queryset containing all banks owned by the current user
        # 2. Apply an SQL aggregation function to the queryset, in this case, Sum() of balance attribute for all banks
        # 3. ['balance__sum'] access result of the aggregation, which is stored in a dictionary with key 'balance__sum'
        total_investment = self.get_queryset().aggregate(Sum('investment'))['investment__sum']  # Second calculation
        context['total_investment'] = floatformat(total_investment, 2)  # rounded to 2 decimal places
        context['total_balance'] = floatformat(total_balance, 2)  # rounded to 2 decimal places
        context['form'] = TransferBetweenBanksForm(self.request.user)  # adds forms for transferring funds between banks
        context['second_form'] = TransferInsideBankForm(self.request.user)  # ...  and accounts
        return context  # returns the updated context dictionary

    def post(self, request, *args, **kwargs):  # method handles form submissions
        form = TransferBetweenBanksForm(request.user, request.POST)  # request.user intended for a form query
        if form.is_valid():  # The form is then validated
            from_bank_id = form.cleaned_data['from_bank']
            to_bank_id = form.cleaned_data['to_bank']
            amount = form.cleaned_data['amount']
            try:  # attempts to retrieve the source and destination banks for the transfer using name and owner fields
                from_bank = Bank.objects.get(name=from_bank_id, owner=request.user)
                to_bank = Bank.objects.get(name=to_bank_id, owner=request.user)
            except Bank.DoesNotExist:  # exception if the specified bank does not exist in the database
                messages.error(request, 'One or both of the banks do not exist or are not owned by you.')
            else:
                if from_bank == to_bank:  # validation to ensure that the user has selected two different banks and ...
                    messages.error(request, 'The source and destination banks must be different.')
                elif from_bank.balance < amount:  # has sufficient balance in the source bank to complete the transfer
                    messages.error(request, 'Insufficient balance.')
                else:
                    from_bank.balance -= amount  # subtracts the transfer amount from the source bank's balance ...
                    to_bank.balance += amount  # and adds it to the destination bank's balance
                    from_bank.save()
                    to_bank.save()  # and saves both banks
                    messages.success(request, 'Your funds have been transferred between the selected banks!')
        else:
            TransferBetweenBanksForm(request.user)  # If request method isn't POST, creates a new instance of form
        # This is done when the user initially navigates to the transfer page

        second_form = TransferInsideBankForm(request.user, request.POST)  # request.user intended for a form query
        if second_form.is_valid():  # If a form for transferring funds within the same bank, it validates the form data
            bank = second_form.cleaned_data['bank']
            source_account = second_form.cleaned_data['source_account']
            to_account = second_form.cleaned_data['to_account']
            amount = second_form.cleaned_data['amount']
            # If any of these checks fail, error is raised:
            if source_account == to_account:
                messages.error(request, 'The source and destination accounts must be different.')
            elif source_account == 'balance' and bank.balance < amount:
                messages.error(request, 'Insufficient balance.')
            elif source_account == 'investment' and bank.investment < amount:
                messages.error(request, 'Insufficient investment.')
            else:  # If all checks are successful, this code transfers the funds between the accounts
                if source_account == 'balance':
                    bank.balance -= amount
                    bank.investment += amount
                else:
                    bank.balance += amount
                    bank.investment -= amount
                bank.save()
                messages.success(request, 'Your funds have been transferred between accounts in the selected bank!')
        else:
            TransferInsideBankForm(request.user)  # If request method isn't POST, creates a new instance of form
        # This is done when the user initially navigates to the transfer page
        return redirect('user-banks')  # redirects the user back to the 'user-banks' view


"""Overall, this form provides a simple way for users to transfer between different accounts within 
the same bank, while ensuring that the transfer amount is valid and the account balances are properly updated."""


# A view function that handles transfers between accounts within the same bank
def transfer_inside_bank(request):  # request argument represents an HTTP request made to the server
    if request.method == 'POST':  # If so, it initializes a new form with the data from the request
        second_form = TransferInsideBankForm(request.user, request.POST)  # request.user intended for a form query
        if second_form.is_valid():  # If a form for transferring funds within the same bank, it validates the form data
            bank = second_form.cleaned_data['bank']  # attribute contains the validated data from the form fields, ...
            source_account = second_form.cleaned_data['source_account']  # which can be used to perform the transfer
            to_account = second_form.cleaned_data['to_account']
            amount = second_form.cleaned_data['amount']
            # If any of these checks fail, error is raised:
            if source_account == to_account:
                messages.error(request, 'The source and destination accounts must be different.')
            elif source_account == 'balance' and bank.balance < amount:
                messages.error(request, 'Insufficient balance.')
            elif source_account == 'investment' and bank.investment < amount:
                messages.error(request, 'Insufficient investment.')
            else:  # If all checks are successful, this code transfers the funds between the accounts
                if source_account == 'balance':
                    bank.balance -= amount
                    bank.investment += amount
                else:
                    bank.balance += amount
                    bank.investment -= amount
                bank.save()
                messages.success(request, 'Your funds have been transferred between accounts in the selected bank!')
    else:
        second_form = TransferInsideBankForm(request.user)  # If request method is not POST, initializes an empty form
    return render(request, 'transfer_inside_bank.html', {'second_form': second_form})


# A view function that handles the transfer of funds between two banks owned by the same user
def transfer_between_banks(request):  # starts by checking if the request method is POST, which indicates that the user
    if request.method == 'POST':  # has submitted a form with data. If so, it initializes a new instance ...
        form = TransferBetweenBanksForm(request.user, request.POST)  # of the form with the data from the request
        if form.is_valid():  # The form is then validated
            from_bank_id = form.cleaned_data['from_bank']
            to_bank_id = form.cleaned_data['to_bank']
            amount = form.cleaned_data['amount']
            try:  # attempts to retrieve the source and destination banks for the transfer using name and owner fields
                from_bank = Bank.objects.get(name=from_bank_id, owner=request.user)
                to_bank = Bank.objects.get(name=to_bank_id, owner=request.user)
            except Bank.DoesNotExist:  # exception if the specified bank does not exist in the database
                messages.error(request, 'One or both of the banks do not exist or are not owned by you.')
            else:
                if from_bank == to_bank:  # validation to ensure that the user has selected two different banks and ...
                    messages.error(request, 'The source and destination banks must be different.')
                elif from_bank.balance < amount:  # has sufficient balance in the source bank to complete the transfer
                    messages.error(request, 'Insufficient balance.')
                else:
                    from_bank.balance -= amount  # subtracts the transfer amount from the source bank's balance ...
                    to_bank.balance += amount  # and adds it to the destination bank's balance
                    from_bank.save()
                    to_bank.save()  # and saves both banks
                    messages.success(request, 'Your funds have been transferred between the selected banks!')
        else:
            messages.error(request, 'Transfer failed. Please check the selected banks and the amount.')
    else:
        form = TransferBetweenBanksForm(request.user)  # If request method isn't POST, creates a new instance of form
        # This is done when the user initially navigates to the transfer page
    return render(request, 'transfer_between_banks.html', {'form': form})  # ... and, finally, renders the template

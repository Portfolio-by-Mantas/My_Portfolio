from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Income
from .forms import IncomeCreateForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


#  A view that lists all Income objects for the currently logged-in user, with the ability to search by various fields
class ListedIncomeByUserListView(LoginRequiredMixin, ListView):  # All views require that the user be logged in
    model = Income
    context_object_name = 'income_lines'
    template_name = 'user_income_lines.html'
    paginate_by = 10

    # Method to filter the list of Income objects based on a search query parameter
    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('query')
        if query:  # To search across several fields for any records that contain the search query
            income = Income.objects.filter(
                Q(category__definition__icontains=query, client=user) |
                Q(source__source__icontains=query, client=user) |
                Q(amount__icontains=query, client=user) |
                Q(notes__icontains=query, client=user) |
                Q(bank__name__icontains=query, client=user)
            )
        else:
            income = Income.objects.filter(client=user)
        return income


# A view that displays the details of a single Income object
class IncomeByUserDetailView(LoginRequiredMixin, DetailView):
    model = Income
    context_object_name = 'income_lines'
    template_name = 'user_income_line.html'

    # This method is used to add extra context data (PDF file) to the template context for rendering the view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income = self.get_object()
        if income.pdf:  # The method checks if the pdf attribute of the Income object is not None
            # The method creates a URL for the PDF file of the Income object ...
            context['pdf_url'] = self.request.build_absolute_uri(income.pdf.url)
            # ... and assigns it to a new key pdf_url in the context dictionary
        return context


# A view that allows the user to create a new Income object
class IncomeByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Income
    success_url = "/portfolio/income_line/new"
    template_name = 'user_income_line_form.html'
    form_class = IncomeCreateForm
    success_message = "Income item was created successfully."

# method is overridden to add the user object to the form's keyword arguments, so that the form can limit the choices
    def get_form_kwargs(self):  # of the bank field to only the banks owned by the current user
        kwargs = super(IncomeByUserCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Override the form_valid method to update the balance field of the Bank model associated with the Income record
    def form_valid(self, form):
        form.instance.client = self.request.user
        response = super().form_valid(form)
        # When creating a new Income record, the balance is increased by the amount of the new record.
        bank = form.cleaned_data['bank']
        amount = form.cleaned_data['amount']
        bank.balance += amount
        bank.save()
        return response


# A view that allows the user to update an existing Income object, require that the user be the owner of the object
class IncomeByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Income
    success_url = "/portfolio/my_income_lines"
    template_name = 'user_income_line_form.html'
    success_message = "Income item was updated successfully."
    form_class = IncomeCreateForm

# method is overridden to add the user object to the form's keyword arguments, so that the form can limit the choices
    def get_form_kwargs(self):  # of the bank field to only the banks owned by the current user
        kwargs = super(IncomeByUserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Override the form_valid method to update the balance field of the Bank model associated with the Income record
    def form_valid(self, form):
        # When updating an existing Income record the balance of bank is increased by the amount of the updated record
        print('Add new amount to bank balance:')  # All the prints are for checking calculations at the terminal
        bank = form.cleaned_data['bank']
        print(f'New bank: {bank}')
        print(f'Balance of new bank: {bank.balance}')
        amount = form.cleaned_data['amount']
        print(f'New amount: {amount}')
        bank.balance += amount
        bank.save()
        print(f'Balance of new bank + new amount after save: {bank.balance}')
        print(50 * '-')

        # Deduct previous amount from bank balance
        income = self.get_object()
        print(f'Previous details of line of income: {income}')
        previous_amount = income.amount
        print(f'Previous amount of income: {previous_amount}')
        previous_bank = income.bank
        print(f'Previous bank: {previous_bank}')
        print(f'Balance of previous bank: {previous_bank.balance}')
        previous_bank.balance -= previous_amount
        previous_bank.save()
        print(f'Balance of previous bank after deduction: {previous_bank.balance}')

        # The function that initiates the update condition is called
        form.instance.client = self.request.user
        response = super().form_valid(form)
        return response

    # Method retrieves the Income object that the view is currently operating on
    def test_func(self):
        income = self.get_object()
        return self.request.user == income.client
    # Method is used to restrict access to views where the user isn't the owner of item being viewed or edited


# A view that allows the user to delete an existing Income object, require that the user be the owner of the object
class IncomeByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Income
    context_object_name = 'income_lines'
    success_url = "/portfolio/my_income_lines"
    template_name = 'user_income_line_delete.html'
    success_message = "Income item was deleted successfully."

    # Method retrieves the Income object that the view is currently operating on,
    def test_func(self):
        income = self.get_object()
        return self.request.user == income.client
    # Method is used to restrict access to views where the user isn't the owner of item being viewed or edited

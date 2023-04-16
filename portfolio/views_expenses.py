from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Expenses
from .forms import ExpensesCreateForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


#  A view that lists all Expenses objects for the currently logged-in user, with the ability to search by various fields
class ListedExpensesByUserListView(LoginRequiredMixin, ListView):  # All views require that the user be logged in
    model = Expenses
    context_object_name = 'expenses_lines'
    template_name = 'user_expenses_lines.html'
    paginate_by = 10

    # Method to filter the list of Expenses objects based on a search query parameter
    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('query')
        if query:  # To search across several fields for any records that contain the search query
            expenses = Expenses.objects.filter(
                Q(category__definition__icontains=query, client=user) |
                Q(seller__seller__icontains=query, client=user) |
                Q(amount__icontains=query, client=user) |
                Q(notes__icontains=query, client=user) |
                Q(bank__name__icontains=query, client=user)
            )
        else:
            expenses = Expenses.objects.filter(client=user)
        return expenses


# A view that displays the details of a single Expenses object
class ExpensesByUserDetailView(LoginRequiredMixin, DetailView):
    model = Expenses
    context_object_name = 'expenses_lines'
    template_name = 'user_expenses_line.html'

    # This method is used to add extra context data (PDF file) to the template context for rendering the view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = self.get_object()
        if expenses.pdf:  # The method checks if the pdf attribute of the Expenses object is not None
            # The method creates a URL for the PDF file of the Expenses object ...
            context['pdf_url'] = self.request.build_absolute_uri(expenses.pdf.url)
            # ... and assigns it to a new key pdf_url in the context dictionary
        return context


# A view that allows the user to create a new Expenses object
class ExpensesByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Expenses
    success_url = "/portfolio/expenses_line/new"
    template_name = 'user_expenses_line_form.html'
    form_class = ExpensesCreateForm
    success_message = "Expenses item was created successfully."

    def get_form_kwargs(self):
        kwargs = super(ExpensesByUserCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Override the form_valid method to update the balance field of the Bank model associated with the Expenses record
    def form_valid(self, form):
        form.instance.client = self.request.user
        response = super().form_valid(form)
        # When creating a new Expenses record, the balance is increased by the amount of the new record.
        bank = form.cleaned_data['bank']
        amount = form.cleaned_data['amount']
        bank.balance -= amount
        bank.save()
        return response


# A view that allows the user to update an existing Expenses object, require that the user be the owner of the object
class ExpensesByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Expenses
    success_url = "/portfolio/my_expenses_lines"
    template_name = 'user_expenses_line_form.html'
    form_class = ExpensesCreateForm
    success_message = "Expenses item was updated successfully."

    def get_form_kwargs(self):
        kwargs = super(ExpensesByUserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Override the form_valid method to update the balance field of the Bank model associated with the Expenses record
    def form_valid(self, form):
        # When updating an existing Expenses record the balance of bank is decreased by the amount of the updated record
        print('Deduct new amount from bank balance:')  # All the prints are for checking calculations at the terminal
        bank = form.cleaned_data['bank']
        print(f'New bank: {bank}')
        print(f'Balance of new bank: {bank.balance}')
        amount = form.cleaned_data['amount']
        print(f'New amount: {amount}')
        bank.balance -= amount
        bank.save()
        print(f'Balance of new bank - new amount after save: {bank.balance}')
        print(50 * '-')

        # Add back previous amount to bank balance
        expenses = self.get_object()
        print(f'Previous details of line of expenses: {expenses}')
        previous_amount = expenses.amount
        print(f'Previous amount of expenses: {previous_amount}')
        previous_bank = expenses.bank
        print(f'Previous bank: {previous_bank}')
        print(f'Balance of previous bank: {previous_bank.balance}')
        previous_bank.balance += previous_amount
        previous_bank.save()
        print(f'Balance of previous bank after refund: {previous_bank.balance}')

        # The function that initiates the update condition is called
        form.instance.client = self.request.user
        response = super().form_valid(form)
        return response

    # Method retrieves the Expenses object that the view is currently operating on
    def test_func(self):
        expenses = self.get_object()
        return self.request.user == expenses.client
    # Method is used to restrict access to views where the user isn't the owner of item being viewed or edited


# A view that allows the user to delete an existing Expenses object, require that the user be the owner of the object
class ExpensesByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Expenses
    context_object_name = 'expenses_lines'
    success_url = "/portfolio/my_expenses_lines"
    template_name = 'user_expenses_line_delete.html'
    success_message = "Expenses item was deleted successfully."

    # Method retrieves the Expenses object that the view is currently operating on
    def test_func(self):
        expenses = self.get_object()
        return self.request.user == expenses.client
    # Method is used to restrict access to views where the user isn't the owner of item being viewed or edited

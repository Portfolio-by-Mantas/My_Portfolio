""" The file code defines a set of class based views related to managing Expenses categories and Sellers for users. The
code imports several Django modules, including mixins for handling user authentication and permissions, as well as
models and forms related to categories of Expenses and Sellers.
The code defines ListViews for displaying a list of Expenses categories and Sellers, DetailViews for displaying details
about specific Expenses categories and Sellers, CreateViews for creating new Expenses categories and Sellers,
UpdateViews for updating existing Expenses categories and Sellers, and DeleteViews for deleting Expenses categories and
Sellers. In total there are 10 views defined.
The views include mixins for handling user authentication and permissions, as well as mixins for displaying success
messages after certain actions are performed (such as creating or updating an Expenses category or Seller). The code
also defines a set of URLs for each view, which can be used to access the views from a web browser.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import ExpensesCategory, Seller
from .forms import SellerCreateForm, ExpensesCategoryCreateForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


# Like in all other views Mixin requires user to be logged-in to access the view
class ListedExpensesCategoryByUserListView(LoginRequiredMixin, ListView):
    model = ExpensesCategory
    context_object_name = 'expenses_categories'
    template_name = 'user_expenses_categories.html'
    paginate_by = 10

    def get_queryset(self):  # overrides the default queryset to return only objects owned by the current user
        user = self.request.user
        return ExpensesCategory.objects.filter(client=user)


class ExpensesCategoryByUserDetailView(LoginRequiredMixin, DetailView):
    model = ExpensesCategory
    context_object_name = 'expenses_categories'
    template_name = 'user_expenses_category.html'


class ExpensesCategoryByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ExpensesCategory
    success_url = "/portfolio/expenses_category/new"
    template_name = 'user_expenses_category_form.html'
    form_class = ExpensesCategoryCreateForm
    success_message = "Expenses category item was created successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class ExpensesCategoryByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = ExpensesCategory
    fields = ['definition']
    success_url = "/portfolio/my_expenses_categories"
    template_name = 'user_expenses_category_form.html'
    success_message = "Expenses category item was updated successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response

    def test_func(self):  # checks whether the user requesting to update an object is the owner of that object
        expenses_category = self.get_object()
        return self.request.user == expenses_category.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class ExpensesCategoryByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = ExpensesCategory
    context_object_name = 'expenses_categories'
    success_url = "/portfolio/my_expenses_categories"
    template_name = 'user_expenses_category_delete.html'
    success_message = "Expenses item was deleted successfully."

    def test_func(self):  # checks whether the user requesting to delete an object is the owner of that object
        expenses_category = self.get_object()
        return self.request.user == expenses_category.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


class ListedSellerByUserListView(LoginRequiredMixin, ListView):
    model = Seller
    context_object_name = 'sellers'
    template_name = 'user_expenses_sellers.html'
    paginate_by = 10

    def get_queryset(self):  # overrides the default queryset to return only objects owned by the current user
        user = self.request.user
        return Seller.objects.filter(client=user)


class SellerByUserDetailView(LoginRequiredMixin, DetailView):
    model = Seller
    context_object_name = 'sellers'
    template_name = 'user_expenses_seller.html'


class SellerByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Seller
    success_url = "/portfolio/seller/new"
    template_name = 'user_expenses_seller_form.html'
    form_class = SellerCreateForm
    success_message = "Seller item was created successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class SellerByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Seller
    fields = ['seller']
    success_url = "/portfolio/my_sellers"
    template_name = 'user_expenses_seller_form.html'
    success_message = "Seller item was updated successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response

    def test_func(self):  # checks whether the user requesting to update an object is the owner of that object
        seller = self.get_object()
        return self.request.user == seller.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class SellerByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Seller
    context_object_name = 'sellers'
    success_url = "/portfolio/my_sellers"
    template_name = 'user_expenses_seller_delete.html'
    success_message = "Expenses item was deleted successfully."

    def test_func(self):  # checks whether the user requesting to delete an object is the owner of that object
        seller = self.get_object()
        return self.request.user == seller.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page

""" The file code defines a set of class based views related to managing Income categories and sources for users. The
code imports several Django modules, including mixins for handling user authentication and permissions, as well as
models and forms related to Income categories and sources.
The code defines ListViews for displaying a list of Income categories and sources, DetailViews for displaying details
about specific Income categories and sources, CreateViews for creating new Income categories and sources, UpdateViews
for updating existing Income categories and sources, and DeleteViews for deleting Income categories and sources. In
total there are 10 views defined.
The views include mixins for handling user authentication and permissions, as well as mixins for displaying success
messages after certain actions are performed (such as creating or updating an Income category or source). The code also
defines a set of URLs for each view, which can be used to access the views from a web browser.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import IncomeSource, IncomeCategory
from .forms import IncomeSourceCreateForm, IncomeCategoryCreateForm
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


# Like in all other views Mixin requires user to be logged-in to access the view
class ListedIncomeCategoryByUserListView(LoginRequiredMixin, ListView):
    model = IncomeCategory
    context_object_name = 'income_categories'
    template_name = 'user_income_categories.html'
    paginate_by = 10

    def get_queryset(self):  # overrides the default queryset to return only objects owned by the current user
        user = self.request.user
        return IncomeCategory.objects.filter(client=user)


class IncomeCategoryByUserDetailView(LoginRequiredMixin, DetailView):
    model = IncomeCategory
    context_object_name = 'income_categories'
    template_name = 'user_income_category.html'


class IncomeCategoryByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncomeCategory
    success_url = "/portfolio/income_category/new"
    template_name = 'user_income_category_form.html'
    form_class = IncomeCategoryCreateForm
    success_message = "Income category item was created successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class IncomeCategoryByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = IncomeCategory
    fields = ['definition']
    success_url = "/portfolio/my_income_categories"
    template_name = 'user_income_category_form.html'
    success_message = "Income category item was updated successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.client = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response

    def test_func(self):  # checks whether the user requesting to update an object is the owner of that object
        income_category = self.get_object()
        return self.request.user == income_category.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class IncomeCategoryByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = IncomeCategory
    context_object_name = 'income_categories'
    success_url = "/portfolio/my_income_categories"
    template_name = 'user_income_category_delete.html'
    success_message = "Income item was deleted successfully."

    def test_func(self):  # checks whether the user requesting to delete an object is the owner of that object
        income_category = self.get_object()
        return self.request.user == income_category.client
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


class ListedIncomeSourceByUserListView(LoginRequiredMixin, ListView):
    model = IncomeSource
    context_object_name = 'income_sources'
    template_name = 'user_income_sources.html'
    paginate_by = 10

    def get_queryset(self):  # overrides the default queryset to return only objects owned by the current user
        user = self.request.user
        return IncomeSource.objects.filter(earner=user)


class IncomeSourceByUserDetailView(LoginRequiredMixin, DetailView):
    model = IncomeSource
    context_object_name = 'income_sources'
    template_name = 'user_income_source.html'


class IncomeSourceByUserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncomeSource
    success_url = "/portfolio/income_source/new"
    template_name = 'user_income_source_form.html'
    form_class = IncomeSourceCreateForm
    success_message = "Income source item was created successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.earner = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class IncomeSourceByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = IncomeSource
    fields = ['source']
    success_url = "/portfolio/my_income_sources"
    template_name = 'user_income_source_form.html'
    success_message = "Income source item was updated successfully."

    def form_valid(self, form):  # defines a method that is called when the form is valid
        form.instance.earner = self.request.user
        response = super().form_valid(form)  # calls the parent class method which saves the form data
        return response  # ... and returns a redirect response

    def test_func(self):  # checks whether the user requesting to update an object is the owner of that object
        income_source = self.get_object()
        return self.request.user == income_source.earner
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page


# TestMixin used to restrict access, the test_func checks if the user meets criteria and can access the view
class IncomeSourceByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = IncomeSource
    context_object_name = 'income_sources'
    success_url = "/portfolio/my_income_sources"
    template_name = 'user_income_source_delete.html'
    success_message = "Income item was deleted successfully."

    def test_func(self):  # checks whether the user requesting to delete an object is the owner of that object
        income_source = self.get_object()
        return self.request.user == income_source.earner
# If the two users do not match, the method returns False, the user will be redirected to a 403 Forbidden error page

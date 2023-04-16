from datetime import date
from django.shortcuts import render
from django.db.models import Q, Sum, Avg, Max, Min
from django.template.defaultfilters import floatformat  # to format the floating-point number
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Income
from .forms import SearchSelectIncomeForm, SearchSelectIncomeForComparisonForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


# Class-based view retrieves objects filtered by search keywords and date, user filters by the logged-in user
class SearchKeywordsIncomeByUserListView(LoginRequiredMixin, ListView):
    model = Income
    context_object_name = 'income'
    template_name = 'user_search_key_income.html'  # retrieved objects are displayed to the user at the template
    paginate_by = 10

    def get_queryset(self):  # filters the objects based on the logged-in user, start and end dates, and search keywords
        user = self.request.user  # retrieves the currently logged-in user
        start_date = self.request.GET.get('start_date')  # retrieves the start date
        end_date = self.request.GET.get('end_date')  # and end date
        keywords = self.request.GET.get('keywords')  # and any search keywords from the request
        # If there are any search keywords, the method splits them into a list of strings and removes ...
        keyword_list = keywords.split(', ') if keywords else []  # ... any whitespace before or after each string

        query = Q(client=user)  # constructs a query object that will be used to filter the Income objects
        # The initial query filters the Income objects by the current user
        if start_date or end_date:  # is specified, the query is updated to include objects within that date range
            start_default = date(1, 1, 1)  # In case only end date selected
            end_default = date.today()  # In case only start date selected
            query &= Q(date__range=[start_date or start_default, end_date or end_default])

        if keyword_list:  # If there are any search keywords, the method constructs another query object
            keyword_query = Q()
            for keyword in keyword_list:  # iterates over each keyword in the list of keywords
                keyword_query |= (  # queries for each keyword are combined using the | operator - OR in Django's syntax
                        Q(category__definition__icontains=keyword) |
                        Q(source__source__icontains=keyword) |
                        Q(amount__icontains=keyword) |
                        Q(notes__icontains=keyword) |
                        Q(bank__name__icontains=keyword)
                )  # For each keyword, the query is updated to include Income objects that match the keyword
            query &= keyword_query
        # the queryset is filtered using the query object and ordered by descending date
        income = Income.objects.filter(query).order_by('-date')
        return income  # The queryset is then returned from the method

    def get_context_data(self, **kwargs):  # adds income stats, number of lines, and total number of lines to context
        context = super().get_context_data(**kwargs)
        total_income = self.get_queryset().aggregate(Sum('amount'))['amount__sum'] or 0  # Zero in case no lines found
        context['total_income'] = floatformat(total_income, 2)  # total income, rounded to 2 decimal places
        avg_income = self.get_queryset().aggregate(Avg('amount'))['amount__avg'] or 0  # Zero in case no lines found
        context['avg_income'] = floatformat(avg_income, 2)  # average income, rounded to 2 decimal places
        max_income = self.get_queryset().aggregate(Max('amount'))['amount__max'] or 0  # Zero in case no lines found
        context['max_income'] = floatformat(max_income, 2)  # max. income, rounded to 2 decimal places
        min_income = self.get_queryset().aggregate(Min('amount'))['amount__min'] or 0  # Zero in case no lines found
        context['min_income'] = floatformat(min_income, 2)  # min. income, rounded to 2 decimal places
        num_income_lines = self.get_queryset().count()  # number of found income lines
        context['num_income_lines'] = num_income_lines
        all_income_lines = Income.objects.all().count()  # number of all income lines by user
        context['all_income_lines'] = all_income_lines
        return context


# Function-based view retrieves objects filtered by search criteria and date, user filters by the logged-in user
@login_required  # The function is decorated - the user must be logged in to access the page
def search_select_income_by_user(request):
    user = request.user
    form = SearchSelectIncomeForm(request.user, request.POST or None)  # filters objects based on the form data
    second_form = SearchSelectIncomeForComparisonForm(request.user, request.POST or None)  # second_form (same logic)
    # None prevents form validation errors during the first load of page when the form data hasn't yet been submitted
    income = Income.objects.filter(client=user).order_by('-date')  # default findings of income, all objects
    income_to_compare = Income.objects.filter(client=user).order_by('-date')

    if request.method == 'POST':  # indicating that a form has been submitted
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            category = form.cleaned_data['category']
            source = form.cleaned_data['source']
            bank = form.cleaned_data['bank']

            query = Q(client=user)  # creates a Django QuerySet object that will be used to retrieve Income objects

            if category:  # ... that match the user's search query, bellow stated all possible criteria
                query &= Q(category=category)

            if source:
                query &= Q(source=source)

            if bank:
                query &= Q(bank=bank)

            if start_date or end_date:
                start_default = date(1, 1, 1)  # In case only end date selected
                end_default = date.today()  # In case only start date selected
                query &= Q(date__range=[start_date or start_default, end_date or end_default])

            income = Income.objects.filter(query).order_by('-date')  # retrieves Income objects that match query

        if second_form.is_valid():  # the same logic as with the first form
            start_date_compare = second_form.cleaned_data['start_date_compare']
            end_date_compare = second_form.cleaned_data['end_date_compare']
            category_compare = second_form.cleaned_data['category_compare']
            source_compare = second_form.cleaned_data['source_compare']
            bank_compare = second_form.cleaned_data['bank_compare']

            query = Q(client=user)

            if category_compare:
                query &= Q(category=category_compare)

            if source_compare:
                query &= Q(source=source_compare)

            if bank_compare:
                query &= Q(bank=bank_compare)

            if start_date_compare or end_date_compare:
                start_default = date(1, 1, 1)  # In case only end date selected
                end_default = date.today()  # In case only start date selected
                query &= Q(date__range=[start_date_compare or start_default, end_date_compare or end_default])

            income_to_compare = Income.objects.filter(query).order_by('-date')

    all_income_lines = Income.objects.filter(client=user).count()  # number of all income lines by user
    num_income_lines = income.count()  # number of found income lines
    num_income_lines_compare = income_to_compare.count()  # number of found income lines to compare
    total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0  # Zero is in case no lines found
    total_income_compare = income_to_compare.aggregate(Sum('amount'))['amount__sum'] or 0
    amount_difference = total_income - total_income_compare  # the difference between the two sets of total income
    avg_income = income.aggregate(Avg('amount'))['amount__avg'] or 0  # Zero is in case no lines found
    avg_income_compare = income_to_compare.aggregate(Avg('amount'))['amount__avg'] or 0
    max_income = income.aggregate(Max('amount'))['amount__max'] or 0  # Zero is in case no lines found
    max_income_compare = income_to_compare.aggregate(Max('amount'))['amount__max'] or 0
    min_income = income.aggregate(Min('amount'))['amount__min'] or 0  # Zero is in case no lines found
    min_income_compare = income_to_compare.aggregate(Min('amount'))['amount__min'] or 0

    context = {
        'form': form,  # adds to the context the form
        'second_form': second_form,  # adds the second_form
        'income': income,  # and data
        'income_to_compare': income_to_compare,  # and data to compare
        'all_income_lines': all_income_lines,  # and number of all income lines
        'num_income_lines': num_income_lines,  # and number of found income lines
        'num_income_lines_compare': num_income_lines_compare,  # and number of found income lines to compare
        'total_income': floatformat(total_income, 2),  # and total income, rounded to 2 decimal places
        'total_income_compare': floatformat(total_income_compare, 2),  # and total income to compare, rounded
        'amount_difference': floatformat(amount_difference, 2),  # and the difference between the sets of total income
        'avg_income':  floatformat(avg_income, 2),  # average income, rounded to 2 decimal places
        'avg_income_compare': floatformat(avg_income_compare, 2),  # average income, rounded to 2 decimal places
        'max_income': floatformat(max_income, 2),  # etc.
        'max_income_compare': floatformat(max_income_compare, 2),
        'min_income': floatformat(min_income, 2),
        'min_income_compare': floatformat(min_income_compare, 2),
    }
    # retrieved objects are displayed to the user at the template
    return render(request, 'user_search_select_income.html', context)

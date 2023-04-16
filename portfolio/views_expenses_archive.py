from datetime import date
from django.shortcuts import render
from django.db.models import Q, Sum, Avg, Max, Min
from django.template.defaultfilters import floatformat  # to format the floating-point number
from django.db.models.functions import TruncMonth
from .models import Expenses
from .forms import ArchiveExpensesForm, ArchiveExpensesByMonthForm
from django.contrib.auth.decorators import login_required


# Function that generates a complex report of expenses data for a given user
@login_required  # The function is decorated - the user must be logged in to access the page
def report_expenses_by_user(request):
    user = request.user  # takes a request object as its argument and uses it to retrieve the user's information
    # creates two forms for filtering expenses data:
    form = ArchiveExpensesForm(request.user, request.POST or None)  # request.user intended for a form query
    monthly_expenses_form = ArchiveExpensesByMonthForm(request.user, request.POST or None)
    # variables that will be used to store info about user's expenses data, default values needed to load the page
    expenses = Expenses.objects.none()
    monthly_data = {}
    total_expenses_period = 0
    num_expenses_lines_period = 0
    avg_expenses_month = 0
    max_expenses_month = 0
    min_expenses_month = 0
    avg_expenses_month_total = 0
    max_expenses_month_total = 0
    min_expenses_month_total = 0

    if request.method == 'POST':  # function processes the form data to filter expenses data based on the user's input
        if form.is_valid():
            start_date = form.cleaned_data['start_date'] or date(1, 1, 1)  # if no start_date will be set default date
            end_date = form.cleaned_data['end_date'] or date.today()  # if no end_date will be set default date - today
            category = form.cleaned_data['category']
            source = form.cleaned_data['source']
            # Q object is used to create a query for Expenses model, filtering the results based on certain conditions
            query = Q(client=user, date__range=[start_date, end_date])  # firstly, client and date range

            if category:
                query &= Q(category=category)  # secondly, if user selects option adds category with 'and' operator

            if source:
                query &= Q(source=source)  # lastly, if user selects option adds source also with 'and' operator
            # Finally, the filter() method is called on the Expenses model with the constructed query
            expenses = Expenses.objects.filter(query)

        if monthly_expenses_form.is_valid():  # selection part in input mirrors the first form
            start_date_report = monthly_expenses_form.cleaned_data['start_date_report'] or date(1, 1, 1)
            end_date_report = monthly_expenses_form.cleaned_data['end_date_report'] or date.today()
            category_report = monthly_expenses_form.cleaned_data['category_report']
            source_report = monthly_expenses_form.cleaned_data['source_report']

            query = Q(client=user, date__range=[start_date_report, end_date_report])

            if category_report:
                query &= Q(category=category_report)

            if source_report:
                query &= Q(seller=source_report)

            expenses_report = Expenses.objects.filter(query)

            # uses the Django 'ORM' (built-in tool for working with databases) aggregation functions to group  ...
            # ... the Expenses objects by month and calculate various statistics on the total expenses for each month.
            expenses_by_month = expenses_report.annotate(  # variable holds the results of expenses_report query
                month=TruncMonth('date')
            ).values('month').annotate(  # annotate() method is used to add new fields to each query result
                total_expenses=Sum('amount'),  # fields are calculated using the aggregation functions, here using 'Sum'
                avg_expenses=Avg('amount'),
                max_expenses=Max('amount'),
                min_expenses=Min('amount')
            )  # month is created using the TruncMonth function, which returns the month value of the date field

            print(expenses_by_month)

            for data in expenses_by_month:  # method 'strftime' allows to format date, in this case it removes days, ...
                month_str = data['month'].strftime('%Y-%m')  # so allows to aggregate data by month
                monthly_data[month_str] = {  # generates a dictionary "monthly_data" that maps each month to ...
                    'total_expenses': data['total_expenses'],  # the total expenses for that month
                    'avg_expenses': data['avg_expenses'],  # etc.
                    'max_expenses': data['max_expenses'],
                    'min_expenses': data['min_expenses']
                }

            print(monthly_data)

            # calculates various statistics about the user's Expenses objects data for month's report:
            num_expenses_lines_period = expenses_report.count()
            # The aggregate function is used to perform a SQL-like aggregation on the filtered data:
            total_expenses_period = expenses_report.aggregate(Sum('amount'))['amount__sum']  # specifies that amount ...
            # field should be summed up for each record, returns sum value as a dict., using ['amount__sum'] key
            avg_expenses_month = expenses_report.aggregate(avg=Avg('amount'))['avg']  # specifies that the amount field
            # should be averaged for each month, returns the average value as a dictionary, using ['avg'] key
            max_expenses_month = expenses_report.aggregate(max=Max('amount'))['max']  # etc.
            min_expenses_month = expenses_report.aggregate(min=Min('amount'))['min']

            avg_expenses_month_total = expenses_by_month.aggregate(avg=Avg('total_expenses'))['avg']  # stats for ...
            max_expenses_month_total = expenses_by_month.aggregate(max=Max('total_expenses'))['max']  # ... whole month
            min_expenses_month_total = expenses_by_month.aggregate(min=Min('total_expenses'))['min']

            print(total_expenses_period)
            print(avg_expenses_month)
            print(max_expenses_month)
            print(min_expenses_month)

            print(avg_expenses_month_total)
            print(max_expenses_month_total)
            print(min_expenses_month_total)

    # calculates various statistics about the user's Expenses objects data from form for main statement:
    num_expenses_lines = expenses.count()
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0  # zero for default value
    avg_expenses = expenses.aggregate(Avg('amount'))['amount__avg'] or 0
    max_expenses = expenses.aggregate(Max('amount'))['amount__max'] or 0
    min_expenses = expenses.aggregate(Min('amount'))['amount__min'] or 0

    context = {  # function passes all data to a context dictionary
        'form': form,
        'monthly_expenses_form': monthly_expenses_form,
        'expenses': expenses,
        'monthly_data': monthly_data,

        'num_expenses_lines': num_expenses_lines,
        'total_expenses': floatformat(total_expenses, 2),  # average expenses, rounded to 2 decimal places
        'avg_expenses': floatformat(avg_expenses, 2),
        'max_expenses': floatformat(max_expenses, 2),
        'min_expenses': floatformat(min_expenses, 2),

        'num_expenses_lines_period': num_expenses_lines_period,
        'total_expenses_period': floatformat(total_expenses_period, 2),
        'avg_expenses_month': floatformat(avg_expenses_month, 2),
        'max_expenses_month': floatformat(max_expenses_month, 2),
        'min_expenses_month': floatformat(min_expenses_month, 2),

        'avg_expenses_month_total': floatformat(avg_expenses_month_total, 2),
        'max_expenses_month_total': floatformat(max_expenses_month_total, 2),
        'min_expenses_month_total': floatformat(min_expenses_month_total, 2),

    }  # dictionary is used to render a template that displays the expenses data for the user

    return render(request, 'user_archive_report_expenses.html', context)

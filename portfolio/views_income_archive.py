from datetime import date
from django.shortcuts import render
from django.db.models import Q, Sum, Avg, Max, Min
from django.template.defaultfilters import floatformat  # to format the floating-point number
from django.db.models.functions import TruncMonth
from .models import Income
from .forms import ArchiveIncomeForm, ArchiveIncomeByMonthForm
from django.contrib.auth.decorators import login_required


# Function that generates a complex report of income data for a given user
@login_required  # The function is decorated - the user must be logged in to access the page
def report_income_by_user(request):
    user = request.user  # takes a request object as its argument and uses it to retrieve the user's information
    # creates two forms for filtering income data:
    form = ArchiveIncomeForm(request.user, request.POST or None)  # request.user intended for a form query
    monthly_income_form = ArchiveIncomeByMonthForm(request.user, request.POST or None)
    # variables that will be used to store info about user's income data, default values needed to load the page
    income = Income.objects.none()
    monthly_data = {}
    total_income_period = 0
    num_income_lines_period = 0
    avg_income_month = 0
    max_income_month = 0
    min_income_month = 0
    avg_income_month_total = 0
    max_income_month_total = 0
    min_income_month_total = 0

    if request.method == 'POST':  # function processes the form data to filter income data based on the user's input
        if form.is_valid():
            start_date = form.cleaned_data['start_date'] or date(1, 1, 1)  # if no start_date will be set default date
            end_date = form.cleaned_data['end_date'] or date.today()  # if no end_date will be set default date - today
            category = form.cleaned_data['category']
            source = form.cleaned_data['source']
            # Q object is used to create a query for Income model, filtering the results based on certain conditions
            query = Q(client=user, date__range=[start_date, end_date])  # firstly, client and date range

            if category:
                query &= Q(category=category)  # secondly, if user selects option adds category with 'and' operator

            if source:
                query &= Q(source=source)  # lastly, if user selects option adds source also with 'and' operator
            # Finally, the filter() method is called on the Income model with the constructed query
            income = Income.objects.filter(query)

        if monthly_income_form.is_valid():  # selection part in input mirrors the first form
            start_date_report = monthly_income_form.cleaned_data['start_date_report'] or date(1, 1, 1)
            end_date_report = monthly_income_form.cleaned_data['end_date_report'] or date.today()
            category_report = monthly_income_form.cleaned_data['category_report']
            source_report = monthly_income_form.cleaned_data['source_report']

            query = Q(client=user, date__range=[start_date_report, end_date_report])

            if category_report:
                query &= Q(category=category_report)

            if source_report:
                query &= Q(source=source_report)

            income_report = Income.objects.filter(query)

            # uses the Django 'ORM' (built-in tool for working with databases) aggregation functions to group  ...
            # ... the Income objects by month and calculate various statistics on the total income for each month.
            income_by_month = income_report.annotate(  # variable holds the results of income_report query
                month=TruncMonth('date')
            ).values('month').annotate(  # annotate() method is used to add new fields to each query result
                total_income=Sum('amount'),  # fields are calculated using the aggregation functions, here using 'Sum'
                avg_income=Avg('amount'),
                max_income=Max('amount'),
                min_income=Min('amount')
            )  # month is created using the TruncMonth function, which returns the month value of the date field

            print(income_by_month)

            for data in income_by_month:  # method 'strftime' allows to format date, in this case it removes days, ...
                month_str = data['month'].strftime('%Y-%m')  # so allows to aggregate data by month
                monthly_data[month_str] = {  # generates a dictionary "monthly_data" that maps each month to ...
                    'total_income': data['total_income'],  # the total income for that month
                    'avg_income': data['avg_income'],  # etc.
                    'max_income': data['max_income'],
                    'min_income': data['min_income']
                }

            print(monthly_data)

            # calculates various statistics about the user's Income objects data for month's report:
            num_income_lines_period = income_report.count()
            # The aggregate function is used to perform a SQL-like aggregation on the filtered data:
            total_income_period = income_report.aggregate(Sum('amount'))['amount__sum']  # specifies that amount ...
            # field should be summed up for each record, returns sum value as a dict., using ['amount__sum'] key
            avg_income_month = income_report.aggregate(avg=Avg('amount'))['avg']  # specifies that the amount field
            # should be averaged for each month, returns the average value as a dictionary, using ['avg'] key
            max_income_month = income_report.aggregate(max=Max('amount'))['max']  # etc.
            min_income_month = income_report.aggregate(min=Min('amount'))['min']

            avg_income_month_total = income_by_month.aggregate(avg=Avg('total_income'))['avg']  # stats for whole month
            max_income_month_total = income_by_month.aggregate(max=Max('total_income'))['max']
            min_income_month_total = income_by_month.aggregate(min=Min('total_income'))['min']

            print(total_income_period)
            print(avg_income_month)
            print(max_income_month)
            print(min_income_month)

            print(avg_income_month_total)
            print(max_income_month_total)
            print(min_income_month_total)

    # calculates various statistics about the user's Income objects data from form for main statement:
    num_income_lines = income.count()
    total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0  # zero for default value
    avg_income = income.aggregate(Avg('amount'))['amount__avg'] or 0
    max_income = income.aggregate(Max('amount'))['amount__max'] or 0
    min_income = income.aggregate(Min('amount'))['amount__min'] or 0

    context = {  # function passes all data to a context dictionary
        'form': form,
        'monthly_income_form': monthly_income_form,
        'income': income,
        'monthly_data': monthly_data,

        'num_income_lines': num_income_lines,
        'total_income': floatformat(total_income, 2),  # average income, floatformat rounds float to 2 decimal places
        'avg_income': floatformat(avg_income, 2),
        'max_income': floatformat(max_income, 2),
        'min_income': floatformat(min_income, 2),

        'num_income_lines_period': num_income_lines_period,
        'total_income_period': floatformat(total_income_period, 2),
        'avg_income_month': floatformat(avg_income_month, 2),
        'max_income_month': floatformat(max_income_month, 2),
        'min_income_month': floatformat(min_income_month, 2),

        'avg_income_month_total': floatformat(avg_income_month_total, 2),
        'max_income_month_total': floatformat(max_income_month_total, 2),
        'min_income_month_total': floatformat(min_income_month_total, 2),

    }  # dictionary is used to render a template that displays the income data for the user

    return render(request, 'user_archive_report_income.html', context)

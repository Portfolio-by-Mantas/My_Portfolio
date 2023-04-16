"""
This app contains a wide variety of views that are based on the following models: Income, Expenses, IncomeCategory,
IncomeSource, ExpensesCategory, Seller, and Bank, as well on the forms for creating and updating instances of these
models. The app have views that creates user-friendly interface with CRUD functionality: listing, creating, updating,
and deleting instances of the models, as well as views handling transfers between banks and within a single bank.
The app's code provides functionality for registering a new user, profile updates, searching Income and Expenses objects
by keywords or criteria and date range, as well as creating archival reports of them. Additionally, the views in the
app have functionality related to user authentication and authorization, including the use of the LoginRequiredMixin
and UserPassesTestMixin mixins.

Due to the size of the code in the views.py file, it is divided into 10 parts and Python file for each was created:
1) Function based views for home page, registration, profile updating - here, at views.py;
2) CRUD functionality for instances of the model: Income - at views_income.py;
3) CRUD functionality for instances of the model: Expenses - at views_expenses.py;
4) CRUD functionality for instances of the models: IncomeCategory, IncomeSource - at views_income_associated.py;
5) CRUD functionality for instances of the models: ExpensesCategory, Seller - at views_expenses_associated.py;
6) Views for searching Income objects, two types search: by keywords or criteria - at views_income_search.py;
7) Views for searching Expenses objects, two types search: by keywords or criteria - at views_expenses_search.py;
8) Views for archival reports of Income objects - at views_income_archive.py;
9) Views for archival reports of Expenses objects - at views_expenses_archive.py;
10) CRUD functionality for instances of the Bank model, as well as views handling transfers between banks and within
a single bank - at views_banks.py.
"""

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm


# For 'home page' view
def home(request):
    text = "Welcome to My_Portfolio"
    context = {
        'text': text,
    }

    return render(request, 'home.html', context=context)


# Decorator to ensure that the data is submitted securely and the cross-site request forgery (CSRF) attack is prevented
@csrf_protect  # It ensures that the request contains a valid CSRF token before processing the form data
def register(request):
    if request.method == "POST":  # This checks if the HTTP method used in the request is POST
        username = request.POST['username']  # This retrieves the value from the POST data submitted by the user.
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #  Password validation, checks if the password and password2 fields match
        if password == password2:
            # This checks if a user with the same username already exists in the User model
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is taken!')
                return redirect('register')  # If username already exists redirects the user back to the registration
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with e-mail {email} is already registered!')
                    return redirect('register')
                else:
                    # This creates a new user with provided details
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # This adds the new user to the 'clients' group by default
                    clients_group = Group.objects.get(name='clients')
                    user.groups.add(clients_group)
                    messages.info(request, f'User {username} successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')  # If passwords does not match redirects the user back to the registration
    return render(request, 'register.html')


"""In summary, this view function handles a user's registration request, checks if the input data is valid, creates a 
new user in the database, adds the new user to a group, and returns appropriate messages based on the success or failure 
of the registration process."""


@login_required  # The function is decorated - the user must be logged in to access the page
def profile(request):  # Function defines a view for a web app's user profile page
    if request.method == "POST":
        # Function creates two form instances with the request data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Profile updated successfully!")
            return redirect('profile')
    else:  # If the request method is not POST, this means that is GET method thus
        # ... the function creates the same form instances but with the current user's instance pre-populated:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    #  ... and renders the profile template with the form instances passed as context
    context = {
        'u_form': user_form,
        'p_form': profile_form,
    }  # Context dictionary contains the two form instances as keys, which will be accessible from the template
    return render(request, 'profile.html', context)

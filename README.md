# <div align="center">My_Portfolio</div>

## <div align="center">Documentation</div>

<details open>
<summary>Summary</summary>
This is a code file for the project My_Portforlio, which is based on Django application named 'portfolio'.
The application consists of multiple models that define different database tables and are used to track and manage income, expenses, bank account's, and related information for clients.
The project includes functionality for uploading and resizing profile pictures, and includes validation to prevent negative input for bank account balances and investment amounts.

The app have views that creates user-friendly interface with CRUD functionality: listing, creating, updating,
and deleting instances of the models, as well as views handling transfers between banks and within a single bank.
The app's code provides functionality for registering a new user, profile updates, searching Income and Expenses objects
by keywords or criteria and date range, as well as creating archival reports of them. Additionally, the views in the
app have functionality related to user authentication and authorization, including the use of the LoginRequiredMixin
and UserPassesTestMixin mixins.


</details>

<details open>
<summary>Install</summary>

Clone repo and install [requirements.txt](https://github.com/Portfolio-by-Mantas/My_Portfolio/blob/main/requirements.txt) in a
[**Python>=3.11.0**](https://www.python.org/) environment

```bash
git clone https://github.com/Portfolio-by-Mantas/My_Portfolio  # clone
cd My_Portfolio
pip install -r requirements.txt  # install
```

</details>

<details open>
<summary>Database</summary>

The default database [db.sqlite3](https://github.com/Portfolio-by-Mantas/My_Portfolio/blob/main/db.sqlite3) 
is provided in the repository. It does not contain sensitive data, it is entered in such a way that the user 
can immediately test the functionality of the website.

Login details for admin - username: Mantas, password: vilnius123;

Login details for user with data: - username: Mantas86, password: vilnius123.

You can delete an existing database and create a new one.
You will then need to create a new administrator account.
```bash
python manage.py migrate  # will automatically create a new database
python manage.py createsuperuser  # will initiate account of superuser creation 
```
</details>


<details open>
<summary>Run the program</summary>

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
</details>

## <div align="center">Contact</div>

For My_Portfolio bug reports and feature requests please contact: mantas.braziunas@gmail.com

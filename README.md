# <div align="center">My_Portfolio</div>

## <div align="center">Documentation</div>

<details open>
<summary>Summary</summary>
This is a code file for the project My_Portfolio, which is based on Django application named 'portfolio'.
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
[**Python>=3.11.0**](https://www.python.org/) environment:


Clone the repository in the Windows terminal:
```bash
git clone https://github.com/Portfolio-by-Mantas/My_Portfolio
```
Open project My_Portfolio using PyCharm.

Create a virtual environment in the PyCharm Settings.

Activate the virtual environment by running the command in the PyCharm Terminal:
```bash
.\venv\Scripts\activate
```

Install the required packages by running the command in the PyCharm Terminal:
```bash
pip install -r requirements.txt
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


After deleting the old database and creating the new one, and creating 'superuser' account:

1) login at http://127.0.0.1:8000/admin/;
2) at http://127.0.0.1:8000/admin/auth/group/ add two user groups: 'admin' and 'clients';
3) assign 'superuser' to both groups in your account;
4) if you will create users on the admin page, assign them the 'clients' group;
5) if you will create users on the website, this will be done automatically.

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

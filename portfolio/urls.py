from django.urls import path
from . import views, views_income, views_expenses, views_income_associated, views_expenses_associated, \
    views_income_search, views_expenses_search, views_banks, views_income_archive, views_expenses_archive

urlpatterns = [
    path('', views.home, name='home'),  # For 'home page' view
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # For Income lines, CRUD functionality, list and detail views provided:
    path('income_line/new', views_income.IncomeByUserCreateView.as_view(), name='income-line-new'),
    path('my_income_lines/', views_income.ListedIncomeByUserListView.as_view(), name='user-income-lines'),
    path('my_income_lines/<int:pk>', views_income.IncomeByUserDetailView.as_view(), name='income-line-detail'),
    path('income_line/<int:pk>/update', views_income.IncomeByUserUpdateView.as_view(), name='income-line-update'),
    path('income_line/<int:pk>/delete', views_income.IncomeByUserDeleteView.as_view(), name='income-line-delete'),

    # For Expenses lines, CRUD functionality, list and detail views provided:
    path('expenses_line/new', views_expenses.ExpensesByUserCreateView.as_view(), name='expenses-line-new'),
    path('my_expenses_lines/', views_expenses.ListedExpensesByUserListView.as_view(), name='user-expenses-lines'),
    path('my_expenses_lines/<int:pk>', views_expenses.ExpensesByUserDetailView.as_view(), name='expenses-line-detail'),
    path('expenses_line/<int:pk>/update', views_expenses.ExpensesByUserUpdateView.as_view(),
         name='expenses-line-update'),
    path('expenses_line/<int:pk>/delete', views_expenses.ExpensesByUserDeleteView.as_view(),
         name='expenses-line-delete'),

    # For Bank objects, CRUD functionality, list and detail views provided:
    path('bank/new', views_banks.BankByUserCreateView.as_view(), name='bank-new'),
    path('my_banks/', views_banks.ListedBanksByUserListView.as_view(), name='user-banks'),
    path('my_banks/<int:pk>', views_banks.BankByUserDetailView.as_view(), name='bank-detail'),
    path('bank/<int:pk>/update', views_banks.BankByUserUpdateView.as_view(), name='bank-update'),
    path('bank/<int:pk>/delete', views_banks.BankByUserDeleteView.as_view(), name='bank-delete'),

    # For transfers between Bank 'accounts', two types - inside bank (among balance and investment) and between banks:
    path('transfer_inside_bank/', views_banks.transfer_inside_bank, name='transfer-inside_bank'),
    path('transfer_between_banks/', views_banks.transfer_between_banks, name='transfer-between_banks'),

    # For IncomeCategory objects, CRUD functionality, list and detail views provided:
    path('income_category/new', views_income_associated.IncomeCategoryByUserCreateView.as_view(),
         name='income-category-new'),
    path('my_income_categories/', views_income_associated.ListedIncomeCategoryByUserListView.as_view(),
         name='user-income-categories'),
    path('my_income_categories/<int:pk>', views_income_associated.IncomeCategoryByUserDetailView.as_view(),
         name='income-category-detail'),
    path('income_category/<int:pk>/update', views_income_associated.IncomeCategoryByUserUpdateView.as_view(),
         name='income-category-update'),
    path('income_category/<int:pk>/delete', views_income_associated.IncomeCategoryByUserDeleteView.as_view(),
         name='income-category-delete'),

    # For IncomeSource objects, CRUD functionality, list and detail views provided:
    path('income_source/new', views_income_associated.IncomeSourceByUserCreateView.as_view(),
         name='income-source-new'),
    path('my_income_sources/', views_income_associated.ListedIncomeSourceByUserListView.as_view(),
         name='user-income-sources'),
    path('my_income_sources/<int:pk>', views_income_associated.IncomeSourceByUserDetailView.as_view(),
         name='income-source-detail'),
    path('income_source/<int:pk>/update', views_income_associated.IncomeSourceByUserUpdateView.as_view(),
         name='income-source-update'),
    path('income_source/<int:pk>/delete', views_income_associated.IncomeSourceByUserDeleteView.as_view(),
         name='income-source-delete'),

    # For ExpensesCategory objects, CRUD functionality, list and detail views provided:
    path('expenses_category/new', views_expenses_associated.ExpensesCategoryByUserCreateView.as_view(),
         name='expenses-category-new'),
    path('my_expenses_categories/', views_expenses_associated.ListedExpensesCategoryByUserListView.as_view(),
         name='user-expenses-categories'),
    path('my_expenses_categories/<int:pk>', views_expenses_associated.ExpensesCategoryByUserDetailView.as_view(),
         name='expenses-category-detail'),
    path('expenses_category/<int:pk>/update', views_expenses_associated.ExpensesCategoryByUserUpdateView.as_view(),
         name='expenses-category-update'),
    path('expenses_category/<int:pk>/delete', views_expenses_associated.ExpensesCategoryByUserDeleteView.as_view(),
         name='expenses-category-delete'),

    # For Seller objects (equivalent to IncomeSource), CRUD functionality, list and detail views provided:
    path('seller/new', views_expenses_associated.SellerByUserCreateView.as_view(), name='seller-new'),
    path('my_sellers/', views_expenses_associated.ListedSellerByUserListView.as_view(), name='user-sellers'),
    path('my_sellers/<int:pk>', views_expenses_associated.SellerByUserDetailView.as_view(), name='seller-detail'),
    path('seller/<int:pk>/update', views_expenses_associated.SellerByUserUpdateView.as_view(), name='seller-update'),
    path('seller/<int:pk>/delete', views_expenses_associated.SellerByUserDeleteView.as_view(), name='seller-delete'),

    # For searching Income and Expenses objects, for both two types of search views - based on keywords and criteria:
    path('search_income_keywords/', views_income_search.SearchKeywordsIncomeByUserListView.as_view(),
         name='search-income-key'),
    path('search_expenses_keywords/', views_expenses_search.SearchKeywordsExpensesByUserListView.as_view(),
         name='search-expenses-key'),
    path('search_income_select/', views_income_search.search_select_income_by_user,
         name='search-income-select'),
    path('search_expenses_select/', views_expenses_search.search_select_expenses_by_user,
         name='search-expenses-select'),
    # For creating archival reports of Income and Expenses objects:
    path('archive_income/', views_income_archive.report_income_by_user, name='archive-income'),
    path('archive_expenses/', views_expenses_archive.report_expenses_by_user, name='archive-expenses'),

]

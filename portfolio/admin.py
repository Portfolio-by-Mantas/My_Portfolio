# All models are registered on the admin page, all variables of all models except Profile are displayed.
from django.contrib import admin
from .models import Profile, Income, Expenses, Bank, IncomeCategory, IncomeSource, ExpensesCategory, Seller


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'amount', 'category', 'source', 'bank')


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'amount', 'category', 'seller', 'bank')


class BankAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'balance', 'investment')


class IncomeSourceAdmin(admin.ModelAdmin):
    list_display = ('earner', 'source')


class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'definition')


class ExpensesCategoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'definition')


class SellerAdmin(admin.ModelAdmin):
    list_display = ('client', 'seller')


admin.site.register(Profile)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(IncomeSource, IncomeSourceAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(ExpensesCategory, ExpensesCategoryAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Bank, BankAdmin)

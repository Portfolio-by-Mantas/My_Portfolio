"""
This is a code file for models. The application consists of
several models and fields that are used to track and manage income, expenses, bank account's, and related information
for clients. Below each class is a brief description of the different model. The code also includes some additional
features such as validation against entering negative amounts or greater dates than today's date. The __str__ method is
also implemented for all models to provide a human-readable representation of each instance.
It should be kept in mind that 4 decorators are associated with the models: User, Profile, Income, Expenses. More
about this in the signals.py file.
"""

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MinValueValidator
from .custom_functions import present_or_past_date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Profile object will be deleted along with User object
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # calls the parent class's 'save' method to save the instance to the database
        # Resizing the profile picture if it is larger than 300x300 pixels
        img = Image.open(self.photo.path)  # function from the Pillow library opens the image
        if img.height > 300 or img.width > 300:  # conditions and parameters
            output_size = (300, 300)
            img.thumbnail(output_size)  # if so, resizes the image using thumbnail() function from the Pillow library
            img.save(self.photo.path)  # saves the resized image to the same path using function from the Pillow


""" This model represents a user profile and contains a one-to-one relationship with the built-in User model provided by 
Django. It also includes an image field for the user's profile picture. """


class Bank(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')

    name = models.CharField('Bank name', max_length=100, default='Other', blank=True,
                            help_text='Enter the name of the bank (e.g. SEB)')
    balance = models.DecimalField('Account balance', max_digits=10, decimal_places=2, default=0, null=True,
                                  validators=[MinValueValidator(0)])  # Validation against entering a negative amount
    investment = models.DecimalField('Investment balance', max_digits=10, decimal_places=2, default=0, null=True,
                                     validators=[MinValueValidator(0)])  # Validation against entering a negative amount

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
        ordering = ['name']


""" This model represents a bank accounts and includes information about the checking account balance and investment 
account balance in a certain bank. It contains a ForeignKey relationship with the built-in User model. """


class IncomeCategory(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    definition = models.CharField('Category definition', max_length=100, default='Other', blank=True,
                                  help_text='Enter the category of the income (e.g. salary)')

    def __str__(self):
        return self.definition

    class Meta:
        verbose_name = 'Income category'
        verbose_name_plural = 'Income categories'
        ordering = ['definition']


""" This model represents different categories of income, such as salary or dividends. It contains a ForeignKey 
relationship with the built-in User model."""


class IncomeSource(models.Model):
    earner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    source = models.CharField('Source of income', max_length=100, default='Other', blank=True,
                              help_text='Enter the source of the income (e.g. university)')

    def __str__(self):
        return self.source

    class Meta:
        verbose_name = 'Source of income'
        verbose_name_plural = 'Sources of income'
        ordering = ['source']


""" This model represents different sources of income, such as an employer (e.g. university) or a particular investment. 
It contains a ForeignKey relationship with the built-in User model. """


class ExpensesCategory(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    definition = models.CharField('Category definition', max_length=100, default='Other', blank=True,
                                  help_text='Enter the category of the expenses (e.g. groceries)')

    def __str__(self):
        return self.definition

    class Meta:
        verbose_name = 'Expenses category'
        verbose_name_plural = 'Expenses categories'
        ordering = ['definition']


""" This model represents different categories of expenses, such as groceries or rent. It contains a ForeignKey 
relationship with the built-in User model. """


class Seller(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    seller = models.CharField('Company or seller', max_length=100, default='Other', blank=True,
                              help_text='Enter the company or seller (e.g. "Maxima")')

    def __str__(self):
        return self.seller

    class Meta:
        verbose_name = 'Company or seller'
        verbose_name_plural = 'Companies and sellers'
        ordering = ['seller']


""" This model represents a company or seller that a client has made a purchase from. It contains a ForeignKey 
relationship with the built-in User model. """


class Income(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    input_date = models.DateTimeField('Date of data input', auto_now_add=True, null=True, blank=True)  # auto-input date
    date = models.DateField('Date of receipt', null=True, blank=False, validators=[present_or_past_date])
    # Validation for date against entering a future date
    amount = models.DecimalField('Amount of income', max_digits=10, decimal_places=2, default=0, blank=True,
                                 validators=[MinValueValidator(0)])  # Validation against entering a negative amount
    category = models.ForeignKey('IncomeCategory', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Income category')
    source = models.ForeignKey('IncomeSource', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Income source')
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Income bank')
    notes = models.TextField('Client notes', max_length=2000, default='There are no additional notes', blank=True)
    pdf = models.FileField(upload_to='income_pdfs', null=True, blank=True, verbose_name='PDF document')

    def __str__(self):
        return f'{self.category} - {self.source}: {self.bank}'

    class Meta:
        verbose_name = "Line of income"
        verbose_name_plural = 'Lines of income'
        ordering = ['-date']


""" This model represents a single instance of Income and includes information about: the date when the income line was 
created; the date of income was received; amount, category, source, and bank account associated with the income. It also 
includes a text field for any notes and a file field for attaching a PDF document. Category, source, and bank variables 
are based on ForeignKey relationships with corresponding models. The income lines will be listed in order of date of 
receipt, starting with the most recent occurrence. """


class Expenses(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Client')
    input_date = models.DateTimeField('Date of data input', auto_now_add=True, null=True, blank=True)  # auto-input date
    date = models.DateField('Date of receipt', null=True, blank=False, validators=[present_or_past_date])
    # Validation for date against entering a future date
    amount = models.DecimalField('Amount of expenses', max_digits=10, decimal_places=2, default=0, blank=True,
                                 validators=[MinValueValidator(0)])  # Validation against entering a negative amount
    category = models.ForeignKey('ExpensesCategory', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Expenses category')
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Company or seller')
    bank = models.ForeignKey('Bank', on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Expenses bank')
    notes = models.TextField('Client notes', max_length=2000, default='There are no additional notes', blank=True)
    pdf = models.FileField(upload_to='expenses_pdfs', null=True, blank=True, verbose_name='PDF document')

    def __str__(self):
        return f'{self.category} - {self.seller}: {self.bank}'

    class Meta:
        verbose_name = 'Line of expenses'
        verbose_name_plural = 'Lines of expenses'
        ordering = ['-date']


""" This model represents a single instance of Expenses and includes information about: the date when the expenses line 
was created; the date of expenses were made; amount, category, seller, and bank account associated with the expenses. It 
also includes a text field for any notes and a file field for attaching a PDF document. Category, seller, and bank 
variables are based on ForeignKey relationships with corresponding models. The expenses lines will be listed in order 
of date of receipt, starting with the most recent occurrence. """

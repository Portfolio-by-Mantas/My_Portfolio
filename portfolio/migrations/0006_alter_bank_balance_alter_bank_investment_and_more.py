# Generated by Django 4.1.7 on 2023-04-10 19:35

import django.core.validators
from django.db import migrations, models
import portfolio.custom_functions


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_alter_bank_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Account balance'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='investment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Investment balance'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount of expenses'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateField(blank=True, null=True, validators=[portfolio.custom_functions.present_or_past_date], verbose_name='Date of receipt'),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount of income'),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(blank=True, null=True, validators=[portfolio.custom_functions.present_or_past_date], verbose_name='Date of receipt'),
        ),
    ]

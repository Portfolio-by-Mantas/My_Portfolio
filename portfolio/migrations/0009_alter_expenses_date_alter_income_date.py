# Generated by Django 4.1.7 on 2023-04-16 16:38

from django.db import migrations, models
import portfolio.custom_functions


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_alter_income_options_alter_expenses_bank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateField(null=True, validators=[portfolio.custom_functions.present_or_past_date], verbose_name='Date of receipt'),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(null=True, validators=[portfolio.custom_functions.present_or_past_date], verbose_name='Date of receipt'),
        ),
    ]

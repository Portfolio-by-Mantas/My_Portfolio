# Generated by Django 4.1.7 on 2023-04-16 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_alter_bank_owner_alter_expenses_client_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='income',
            options={'ordering': ['-date'], 'verbose_name': 'Line of income', 'verbose_name_plural': 'Lines of income'},
        ),
        migrations.AlterField(
            model_name='expenses',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio.bank', verbose_name='Expenses bank'),
        ),
        migrations.AlterField(
            model_name='income',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio.bank', verbose_name='Income bank'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-01 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_role_socialrole_alter_account_options_and_more'),
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='user',
            field=models.ForeignKey(help_text='The user who performed the search.', on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
    ]
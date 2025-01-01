# Generated by Django 5.1.4 on 2025-01-01 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_role_socialrole_alter_account_options_and_more'),
        ('tunes', '0002_alter_wikiadmin_options_alter_wikiadmin_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikiadmin',
            options={},
        ),
        migrations.AlterModelManagers(
            name='wikiadmin',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='privilege',
            name='title',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='admin_names',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='current_date',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='email',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='wikiadmin',
            name='username',
        ),
        migrations.AddField(
            model_name='wikiadmin',
            name='can_validate_content',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='privilege',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Custom user to which privilege applies if applicable.', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
    ]
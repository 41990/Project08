# Generated by Django 5.1.4 on 2025-01-01 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_role_socialrole_alter_account_options_and_more'),
        ('content', '0002_sitebookmark_siteemoji_sitereport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(help_text='User who made the comment.', on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
        migrations.AlterField(
            model_name='sitebookmark',
            name='user',
            field=models.ForeignKey(help_text='User who makes the bookmark', on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
        migrations.AlterField(
            model_name='siteemoji',
            name='user',
            field=models.ForeignKey(help_text='User who makes the emoji reaction', on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
        migrations.AlterField(
            model_name='sitereaction',
            name='user',
            field=models.ForeignKey(help_text='User who makes the reaction', on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
        migrations.AlterField(
            model_name='sitereport',
            name='user',
            field=models.ForeignKey(blank=True, help_text='User who makes the report', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.visitor'),
        ),
    ]
# Generated by Django 5.1.4 on 2024-12-28 20:37

import content.models
import django.db.models.deletion
import forums.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=True, help_text='Indicates if the object is valid.')),
                ('title', models.CharField(help_text='Title of the forum.', max_length=50)),
                ('description', models.FileField(help_text='File describing the forum content.', upload_to=forums.models.forum_data_desc_dir_path)),
                ('category', models.CharField(choices=[('CAT_0', 'Choose'), ('CAT_1', 'Category 1'), ('CAT_2', 'Category 2'), ('CAT_3', 'Category 3'), ('CAT_4', 'Category 4'), ('CAT_5', 'Category 5'), ('CAT_6', 'Category 6')], default='CAT_0', help_text='Forum category.', max_length=10)),
                ('pub_date', models.DateTimeField(auto_now=True, help_text='Date when the forum was published.')),
                ('current_date', models.DateField(auto_now=True, help_text='Last updated date.')),
                ('account', models.ForeignKey(help_text='Associated account for the forum.', on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=(models.Model, content.models.ReactionMixin),
        ),
    ]

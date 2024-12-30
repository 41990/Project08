# Generated by Django 5.1.4 on 2024-12-28 20:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('message', 'Message'), ('alert', 'Alert'), ('reminder', 'Reminder')], help_text='Type of notification.', max_length=20)),
                ('content', models.TextField(help_text='The content of the notification.')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='Time when the notification was sent.')),
                ('read', models.BooleanField(default=False, help_text='Whether the notification has been read.')),
                ('recipient', models.ForeignKey(help_text='User receiving the notification.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('read', 'Read'), ('dismissed', 'Dismissed')], help_text='Action performed on the notification.', max_length=20)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='Time when the action was performed.')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='notifications.notification')),
                ('user', models.ForeignKey(help_text='User who interacted with the notification.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

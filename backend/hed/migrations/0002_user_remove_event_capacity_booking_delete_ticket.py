# Generated by Django 5.1.2 on 2025-04-13 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('gmail', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=20, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('profilepictureurl', models.TextField(blank=True, null=True)),
                ('role', models.CharField(choices=[('Customer', 'Customer'), ('EventOrganizer', 'EventOrganizer'), ('Admin', 'Admin')], default='Customer', max_length=20)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_banned', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='capacity',
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hed.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hed.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]

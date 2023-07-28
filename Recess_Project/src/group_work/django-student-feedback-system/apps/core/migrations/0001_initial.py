# Generated by Django 3.2.6 on 2023-07-27 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('student_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('course', models.CharField(max_length=100)),
                ('enrollment_year', models.PositiveIntegerField()),
                ('password', models.CharField(default='pbkdf2_sha256$260000$ejBg3Kg7W0QOA3k7qBY8ou$XnF4jUjEKutAQEBO92CuH92sYXitqGFrYPkkOVhJ2tw=', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
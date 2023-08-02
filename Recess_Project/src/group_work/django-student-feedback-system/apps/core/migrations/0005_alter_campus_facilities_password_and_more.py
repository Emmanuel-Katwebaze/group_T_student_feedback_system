# Generated by Django 4.2.3 on 2023-07-31 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_campus_facilities_facilitiesmanager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus_facilities',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$Nk987k1ixg4wQZCCEWHe5J$VUwIu26/ScIMcDYfVv9+wnDAyooiSX+2uTKmqTd9a84=', max_length=128),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$pijc3FV6aeET9T8HZ5VyOO$X8QubI1WKUlWg3dXyupVWd3SFgxaf9ZM4dR4Hy4GYcE=', max_length=128),
        ),
    ]
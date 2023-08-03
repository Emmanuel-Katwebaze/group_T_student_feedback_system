# Generated by Django 4.2.3 on 2023-08-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230726_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus_facilities',
            fields=[
                ('campus_facilitiesID', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('contact_information', models.CharField(max_length=100)),
                ('availability', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('hours_of_operation', models.CharField(max_length=100)),
                ('password', models.CharField(default='pbkdf2_sha256$600000$4P5oQexl95qIxD2zbihLXz$lv8OkOicQGURhKBj30FdI4xaZXpMJQXyj8v9/Zi2d3Y=', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('course_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('course_code', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=100)),
                ('credit_hours', models.IntegerField()),
                ('password', models.CharField(default='pbkdf2_sha256$600000$41YNUlBf6U7URHwz2cCFEU$++kmKpNa5q60F4B5h1lvHq5dQJePChehl7VCIo5ldpM=', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='facilitiesManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('instructor_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('department', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$94dEbrcyjXskIty1JIOj82$BsMK54hfkrK7kFgmR3JhAWSlVz8sLX+AaISGqE888AM=', max_length=128),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-31 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_campus_facilities_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus_facilities',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$EyjNszhQi53uSwbCuXU8hE$rabky0uG98zvHlHM7dCI3dCgKiHXPuuc6hZlYTjUW/c=', max_length=128),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$xpOskcpusRiWxlZAzIo3BI$NHjsKPOq7b+2KfNDro7K9Em1ukjPVHZMhmZ9YJflq3w=', max_length=128),
        ),
    ]
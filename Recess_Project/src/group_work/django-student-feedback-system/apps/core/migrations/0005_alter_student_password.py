# Generated by Django 4.2.3 on 2023-07-31 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_course_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$UJMx3tiZI8MWiHVlrFPrRX$/FyVLkCnn+MJzklv8Ad/pdophDG72X7YIX1hgvqsJHs=', max_length=128),
        ),
    ]
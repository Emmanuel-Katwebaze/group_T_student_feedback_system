# Generated by Django 4.2.3 on 2023-08-01 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_course_password_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$JLVNqTgn7FSuH1ZOqcXC3Z$5KL4fQ+l4TI13cFef9jTQyuprGQq+HoFjtosMmwgV4Y=', max_length=128),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$0C5Bb3IamZUfeNMPl3GjDf$vNDzcmozTw9g+WRXv8WBnEmkmR2edODp8QKHTtbJNRg=', max_length=128),
        ),
    ]

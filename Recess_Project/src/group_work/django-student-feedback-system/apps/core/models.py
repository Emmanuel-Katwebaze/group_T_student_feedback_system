from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
 


class StudentManager(BaseUserManager):
    def create_user(self, **extra_fields):
        student = self.model(**extra_fields)
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    student_id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    enrollment_year = models.PositiveIntegerField()

    # New field for password storage
    password = models.CharField(max_length=128, default=make_password('12345678'))

    # Set the manager for the custom User model
    objects = StudentManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'student_id'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def check_password(self, raw_password):
        # Compare the provided raw_password with the stored password hash
        return check_password(raw_password, self.password)



# Instructor 
class InstructorManager(BaseUserManager):
    def create_instructor(self, **extra_fields):
        instructor = self.model(**extra_fields)
        instructor.save(using=self._db)
        return instructor

class Instructor(AbstractBaseUser):
    instructor_id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)

    # New field for password storage

    # Set the manager for the custom User model
    objects = InstructorManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'instructor_id'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


#Course Model

class CourseManager(models.Manager):
    def create_course(self, **extra_fields):
        course = self.model(**extra_fields)
        course.save(using=self._db)
        return course

class Course(AbstractBaseUser):
    course_id = models.AutoField(primary_key=True, unique=True)
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    credit_hours = models.IntegerField()
    # New field for password storage
    password = models.CharField(max_length=128, default=make_password('12345678'))

    # Set the manager for the custom User model
    objects = CourseManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'course_id'

    def __str__(self):
        return self.course_name
    
    
    # campus facilities

class facilitiesManager(AbstractBaseUser):
    def create_user(self, **extra_fields):
        facilities = self.model(**extra_fields)
        facilities.save(using=self._db)
        return facilities

class Campus_facilities(models.Model):
    campus_facilitiesID = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    # availability = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    hours_of_operation= models.CharField(max_length=100)
    # enrollment_year = models.PositiveIntegerField()

    # New field for password storage
    password = models.CharField(max_length=128, default=make_password('12345678'))

    # Set the manager for the custom User model
    objects = facilitiesManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'campus_facilitiesID'

    def __str__(self):
        return f"{self.name}"
    


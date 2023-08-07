from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class StudentManager(BaseUserManager):
    def create_user(self, **extra_fields):
        student = self.model(**extra_fields)
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser, PermissionsMixin):
    student_id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    enrollment_year = models.PositiveIntegerField()

    # New field for password storage
    password = models.CharField(
        max_length=128, default=make_password('12345678'))

    # Required fields for Django's admin interface
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Set the manager for the custom User model
    objects = StudentManager()

    # Use the student_id as the unique identifier for authentication
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'course', 'enrollment_year']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        # Compare the provided raw_password with the stored password hash
        return check_password(raw_password, self.password)

# Set unique related_name attributes to avoid clashes with default User model
Student.groups.field.remote_field.related_name = 'student_groups'
Student.user_permissions.field.remote_field.related_name = 'student_user_permissions'


# Instructor 

class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


#Course Model

class Course(models.Model):
    course_id = models.AutoField(primary_key=True, unique=True)
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    credit_hours = models.IntegerField()

    def __str__(self):
        return self.course_name
    
    
# campus facilities

class CampusFacility(models.Model):
    campus_facilitiesID = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    availability = models.CharField(max_length=100)
    hours_of_operation= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class FormCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Form(models.Model):
    title = models.CharField(max_length=100)
    categoryID = models.ForeignKey(FormCategory, on_delete=models.CASCADE)
    
    # New fields for generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Add GenericRelation for reverse querying
    responses = GenericRelation('StudentResponse')

    def __str__(self):
        return f"{self.title} CategoryID - {self.categoryID}"


class Question(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    question_type = models.CharField(
        max_length=20)  # 'text' or 'multipleChoice'
    options = models.CharField(max_length=1000, blank=True, null=True)


class StudentResponse(models.Model):
    form = models.ForeignKey('Form', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    # You can adjust the field size as needed
    student_ID = models.BigIntegerField()
    # Use TextField for longer responses
    response_text = models.TextField(blank=True, null=True)
    response_choice = models.CharField(
        max_length=100, blank=True, null=True)  # For multiple choice questions
    
    # New fields for generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.student_ID}'s response to {self.question}"



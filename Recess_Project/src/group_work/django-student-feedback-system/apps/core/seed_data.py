# seed_data.py

from apps.core.models import Course, Instructor, CampusFacility, FormCategory

def seed_courses():
    course_data = [
        {
            'course_name': 'Software Engineering',
            'course_code': 'BSSE',
            'department': 'Networks',
            'credit_hours': 60
        },
        {
            'course_name': 'Civil Engineering',
            'course_code': 'BSCIV',
            'department': 'Engineering',
            'credit_hours': 60
        },
        # Add more course data here
    ]

    for data in course_data:
        Course.objects.create(**data)

def seed_instructors():
    instructor_data = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'department': 'Engineering'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'department': 'Networks'
        },
        # Add more instructor data here
    ]

    for data in instructor_data:
        Instructor.objects.create(**data)

def seed_campus_facilities():
    facilities_data = [
        {
            'name': 'Hospital',
            'location': 'Location X',
            'contact_information': '07777777777',
            'description': 'A comfortable well facilitated hospital',
            'availability': 'Available',
            'hours_of_operation': '24/7'
        },
        {
            'name': 'Library',
            'location': 'Location Y',
            'contact_information': '07777777777',
            'description': 'A comfortable reading environment',
            'availability': 'Available',
            'hours_of_operation': '8am-5pm weekdays'
        },
        # Add more facility data here
    ]

    for data in facilities_data:
        CampusFacility.objects.create(**data)
        
def seed_form_categories():
    categories_data = [
        {
            'category': 'instructors',
        },
        {
            'category': 'courses',
        },
        {
            'category': 'facilities',
        },
    ]

    for data in categories_data:
        FormCategory.objects.create(**data)



# seed_data.py  python manage.py runscript apps.core.seed_data -v2, the seed file should be in the same directory as the models
# pip install django-extensions
# INSTALLED_APPS = [
#     # other installed apps...
#     'django_extensions',
# ]


def run():
    seed_courses()
    seed_instructors()
    seed_campus_facilities()
    seed_form_categories()

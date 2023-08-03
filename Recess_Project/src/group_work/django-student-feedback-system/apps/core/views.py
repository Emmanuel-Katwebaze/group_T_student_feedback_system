from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Student, Course,Campus_facilities
from django.contrib.auth.hashers import make_password



def admin_signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        admin = auth.authenticate(username=username, password=password)
        print(admin)
        if admin is not None:
            auth.login(request, admin)
            return redirect('admin-dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('admin-signin')
    else:
        return render(request, 'project_admin/admin_auth/signin.html')


@login_required(login_url='admin-signin')
def dashboard(request):
    # Get the total number of student records in the database
    total_students = Student.objects.count()

    context = {
        'segment': 'index',
        'total_students': total_students,  # Add the count to the context
    }

    return render(request, 'project_admin/index.html', context)


@login_required(login_url='admin-signin')
def admin_students(request):

    student_records = Student.objects.all()
    context = {'segment': 'students', 'student_records': student_records}

    return render(request, 'project_admin/students.html', context)


@login_required(login_url='admin-signin')
@require_POST
def add_student(request):
    first_name = request.POST['new_first_name']
    student_id = request.POST['new_student_id']
    last_name = request.POST['new_last_name']
    email = request.POST['new_email']
    course = request.POST['new_course']
    enrollment_year = request.POST['new_enrollment_year']
    password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    # Check if passwords match
    if password != confirm_password:
        messages.error(request, 'Passwords do not match.')
        return redirect('admin-dashboard-students')

    # Validate the uniqueness of the email
    if Student.objects.filter(email=email).exists():
        messages.error(request, 'Email address is already in use.')
        return redirect('admin-dashboard-students')

    # Create a new Student object and save it to the database
    student = Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        course=course,
        enrollment_year=enrollment_year,
        password=make_password(password)
    )
    if student is not None:
        student.save()
        messages.success(request, 'New student added successfully.')
    else:
        messages.error(request, 'Error adding student.')
    return redirect('admin-dashboard-students')


@login_required(login_url='admin-signin')
@require_POST
def delete_student(request, pk):
    student = Student.objects.get(student_id=pk)
    student.delete()
    messages.success(
        request, "Student Deleted Successfully")
    return redirect('admin-dashboard-students')


@login_required(login_url='admin-signin')
@require_POST
def update_student(request, student_id):
    # Retrieve the student object based on the provided student_id
    student = get_object_or_404(Student, pk=student_id)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    course = request.POST['course']
    enrollment_year = request.POST['enrollment_year']
    password_edit = request.POST['password_edit']

    try:
            # Check if the new password is not already hashed
        if password_edit and not password_edit.startswith('pbkdf2_sha256'):
            student.password = make_password(password_edit)
        else:
            # If the password is already hashed or not provided, use the original form data
            student.password = password_edit

        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.course = course
        student.enrollment_year = enrollment_year
        student.save()
        messages.success(request, "Student Update Successfully")
    except:
        messages.error(request, "Error Updating Student")

    return redirect('admin-dashboard-students')

@login_required(login_url='admin-signin')
def admin_courses(request):

    course_records = Course.objects.all()
    context = {'segment': 'courses', 'course_records': course_records}

    return render(request, 'project_admin/courses.html', context)


@login_required(login_url='admin-signin')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin-signin')

@login_required(login_url='admin-signin')
@require_POST
def add_course(request):
    course_name = request.POST['new_course_name']
    course_code = request.POST['new_course_code']
    department = request.POST['new_department']
    credit_hours = request.POST['new_credit_hours']
    
    # Create a new Course object and save it to the database
    course = Course(
        course_name=course_name,
        course_code=course_code,
        department=department,
        credit_hours=credit_hours
        
    )
    if course is not None:
        course.save()
        messages.success(request, 'New Course added successfully.')
    else:
        messages.error(request, 'Error adding course.')
    return redirect('admin-dashboard-courses')

@login_required(login_url='admin-signin')
@require_POST
def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    course.delete()
    messages.success(request, "Course Deleted Successfully")
    return redirect('admin-dashboard-courses')

@login_required(login_url='admin-signin')
@require_POST
def update_course(request, course_id):
    # Retrieve the course object based on the provided course_id
    course = get_object_or_404(Course, pk=course_id)
    course_name = request.POST['course_name']
    course_code = request.POST['course_code']
    department = request.POST['department']
    credit_hours=request.POST['credit_hours']

    try:
        course.course_name = course_name
        course.course_code = course_code
        course.department = department
        course.credit_hours=credit_hours
        course.save()
        messages.success(request, "Course Updated Successfully")
    except:
        messages.error(request, "Error Updating Course")

    return redirect('admin-dashboard-courses')



# Campus facilities

@login_required(login_url='admin-signin')
def admin_facilities(request):
    facilities_records = Campus_facilities.objects.all()
    context = {'segment': 'facilities', 'facilities_records': facilities_records}
    return render(request, 'project_admin/Campus_facilities.html', context)




@login_required(login_url='admin-signin')
@require_POST
def add_facilities(request):
    campus_facilitiesID = request.POST['campus_facilitiesID']
    name = request.POST['name']
    description= request.POST['description']
    availability = request.POST['availability']
    location = request.POST['location']
    contact_information = request.POST['contact_information']
    hours_of_operation= request.POST['hours_of_operation']
    
    # Create a new Course object and save it to the database
    campus_facilities = Campus_facilities(
        campus_facilitiesID=campus_facilitiesID,
        name=name,
        availability=availability,
        location=location,
        contact_information=contact_information,
        hours_of_operation=hours_of_operation,
        description=description
        
    )
    if campus_facilities is not None:
        campus_facilities.save()
        messages.success(request, 'New facility added successfully.')
    else:
        messages.error(request, 'Error adding facility.')
    return redirect('admin-dashboard-facilities')



@login_required(login_url='admin-signin')
@require_POST
def delete_facility(request, pk):
    # Similar to delete_student function but for Campus_facities model
    facility = get_object_or_404(Campus_facilities, campus_facilitiesID=pk)
    facility.delete()
    messages.success(request, "Facility Deleted Successfully")
    return redirect('admin-dashboard-facilities')


@login_required(login_url='admin-signin')
@require_POST
def update_facility(request, facility_id):
    # Retrieve the facility object based on the provided facility_id
    facility = get_object_or_404(Campus_facilities, campus_facilitiesID=facility_id)
    name = request.POST['name']
    contact_information = request.POST['contact_information']
    location = request.POST['location']
    availability = request.POST['availability']
    description = request.POST['description']
    hours_of_operation = request.POST['hours_of_operation']
    

    

    facility.name = name
    facility.location = location
    facility.availability = availability
    facility.contact_information = contact_information
    facility.description = description
    facility.hours_of_operation = hours_of_operation
    facility.save()
    

    if facility is not None:
        facility.save()
        messages.success(request, ' Facility updated successfully.')
    else:
        messages.error(request, 'Error updating facility.')
    return redirect('admin-dashboard-facilities')





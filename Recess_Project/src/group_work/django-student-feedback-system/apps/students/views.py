from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.core.models import Student, Question, StudentResponse, Form, CampusFacility, Instructor, Course
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_number')
        password = request.POST.get('password')
        try:
            user = authenticate(request, student_id=student_id, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('signin')
        except Exception as e:
            messages.error(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'students/students_auth/signin.html')


def signup(request):
    if request.method == 'POST':
        # Get form data from POST request
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        enrollment_year = request.POST.get('enrollment_year')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')  # Redirect to the sign-up page

        # Validate the uniqueness of the email
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already in use.')
            return redirect('signup')  # Redirect to the sign-up page

        try:
            # Create the student with the provided data
            student = Student.objects.create(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                course=course,
                enrollment_year=enrollment_year,
                password=make_password(password)
            )
            messages.success(request, 'You have successfully signed up.')
            request.session['authenticated_student_id'] = student.student_id
            return redirect('student_dashboard')
        except Exception as e:
            # Handle validation errors
            messages.error(request, "Validation Error")
            return redirect('signup')  # Redirect to the sign-up page

    return render(request, 'students/students_auth/signup.html')


@login_required(login_url=signin)
def student_dashboard(request):
    student = request.user
    # Get the responses for the current student using their email
    form_responsed_to = StudentResponse.objects.filter(
        student_ID=student.student_id).values_list('form_id', flat=True).distinct().count()
    form_count = Form.objects.all().count()
    unanswered_forms = form_count - form_responsed_to 
    context = {'segment': 'index', 'form_responsed_to': form_responsed_to, 'unanswered_forms':unanswered_forms}
    return render(request, 'students/index.html', context)



def student_logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('signin')


@login_required(login_url='signin')
def student_view_form(request, form_id):
    try:
        form = Form.objects.get(id=form_id)
        questions = Question.objects.filter(form=form)
        for question in questions:
            if question.question_type == 'multipleChoice':
                # Convert the 'options' string to a Python object
                options = eval(question.options)
                question.options = options
        if request.method == 'POST':
            for question in questions:
                response = StudentResponse(
                    form=form,
                    question=question,
                    student_ID=request.POST.get('student_ID', ''),
                    response_text=request.POST.get(
                        f'response_text_{question.id}', ''),
                    response_choice=request.POST.get(
                        f'response_choice_{question.id}', '')
                )
                # Set the content type and object_id before saving
                response.content_type = ContentType.objects.get_for_model(Form)
                response.object_id = form.id
                response.save()
            messages.success(request, 'Form Submitted Successfully')
            return redirect('student_view_all_forms')
        return render(request, 'students/student_view_form.html', {'form': form, 'questions': questions, 'segment': 'forms'})
    except Form.DoesNotExist:
        return redirect('student_view_all_forms')

@login_required(login_url='signin')
def student_view_all_forms(request):
    query = request.GET.get('q')
    forms = Form.objects.all()

    if query:
        # Perform a case-insensitive search for forms based on title
        forms = forms.filter(
            Q(title__icontains=query)
        )

        # Filter by content_type__model and object_id fields
        content_type_query = ContentType.objects.filter(model__icontains=query)
        forms |= Form.objects.filter(content_type__in=content_type_query)

        # Filter by the first name, last name, and department of the instructor
        instructor_query = Instructor.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(department__icontains=query)
        )
        content_type_instructor = ContentType.objects.get_for_model(Instructor)
        forms |= Form.objects.filter(
            content_type=content_type_instructor, object_id__in=instructor_query)

        # Filter by the name of the facility
        facility_query = CampusFacility.objects.filter(
            facility_name__icontains=query)
        content_type_facility = ContentType.objects.get_for_model(
            CampusFacility)
        forms |= Form.objects.filter(
            content_type=content_type_facility, object_id__in=facility_query)

        # Filter by the course name, course code, or department of the course
        course_query = Course.objects.filter(
            Q(course_name__icontains=query) |
            Q(course_code__icontains=query) |
            Q(department__icontains=query)
        )
        content_type_course = ContentType.objects.get_for_model(Course)
        forms |= Form.objects.filter(
            content_type=content_type_course, object_id__in=course_query)

    # Get the currently logged-in student
    student = request.user

    # Get the responses for the current student using their email
    form_responses = StudentResponse.objects.filter(
        student_ID=student.student_id).values_list('form_id', flat=True)

    # Pass the student's email and the responses to the template
    context = {
        'segment': 'forms',
        'forms': forms,
        'user_email': student.email,
        'form_responses': form_responses,
        'segment': 'forms'
    }

    return render(request, 'students/student_view_all_forms.html', context)

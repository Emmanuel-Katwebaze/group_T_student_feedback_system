from django.http import HttpResponse
import csv
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Student, Course, CampusFacility, Instructor, FormCategory, Form, Question, StudentResponse
from django.contrib.auth.hashers import make_password
from .forms import QuestionForm
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
import matplotlib
matplotlib.use('Agg')


def admin_signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        admin = auth.authenticate(username=username, password=password)
        print(admin)
        if admin is not None:
            auth.login(request, admin)
            messages.success(request, 'Login Successful')
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('admin-signin')
    else:
        return render(request, 'project_admin/admin_auth/signin.html')


@login_required(login_url='admin-signin')
def dashboard(request):
    # Get the total number of student records in the database
    total_students = Student.objects.count()
    # Get the total number of Instructor records in the database
    total_instructors = Instructor.objects.all().count()
    total_courses = Course.objects.all().count()
    total_facilities = CampusFacility.objects.all().count()
    total_forms = Form.objects.all().count()
    total_answered_forms = StudentResponse.objects.values_list(
        'form_id', flat=True).distinct().count()

    context = {
        'segment': 'index',
        'total_students': total_students,  # Add the count to the context
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_facilities': total_facilities,
        'total_forms': total_forms,
        'total_answered_forms': total_answered_forms
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
        messages.success(request, "Student Updated Successfully")
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
    messages.success(request, "Logout Successful")
    return redirect('admin-signin')

    # --=========================--
    #           Instructors
    # --=======================---


@login_required(login_url='admin-signin')
def admin_instructors(request):

    instructor_records = Instructor.objects.all()
    context = {'segment': 'instructors',
               'instructor_records': instructor_records}

    return render(request, 'project_admin/instructors.html', context)

# Add Instructor to the database


@login_required(login_url='admin-signin')
@require_POST
def add_instructor(request):
    first_name = request.POST['new_first_name']
    last_name = request.POST['new_last_name']
    email = request.POST['new_email']
    department = request.POST['new_department']

    # Validate the uniqueness of the email
    if Instructor.objects.filter(email=email).exists():
        messages.error(request, 'Email address is already in use.')
        return redirect('admin-dashboard-instructors')

    # Create a new Instructor object and save it to the database
    instructor = Instructor(
        first_name=first_name,
        last_name=last_name,
        email=email,
        department=department,
    )
    if instructor is not None:
        instructor.save()
        messages.success(request, 'New Instructor added successfully.')
    else:
        messages.error(request, 'Error adding Instructor.')
    return redirect('admin-dashboard-instructors')


# delete Instructor

@login_required(login_url='admin-signin')
@require_POST
def delete_instructor(request, pk):
    instructor = Instructor.objects.get(instructor_id=pk)
    instructor.delete()
    messages.success(
        request, "Instructor Deleted Successfully")
    return redirect('admin-dashboard-instructors')

# Update Instructor


@login_required(login_url='admin-signin')
@require_POST
def update_instructor(request, instructor_id):
    # Retrieve the student object based on the provided student_id
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    department = request.POST['department']

    try:

        instructor.first_name = first_name
        instructor.last_name = last_name
        instructor.email = email
        instructor.department = department
        instructor.save()
        messages.success(request, "Instructor Updated Successfully")
    except:
        messages.error(request, "Error Updating Student")

    return redirect('admin-dashboard-instructors')


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
    credit_hours = request.POST['credit_hours']

    try:
        course.course_name = course_name
        course.course_code = course_code
        course.department = department
        course.credit_hours = credit_hours
        course.save()
        messages.success(request, "Course Updated Successfully")
    except:
        messages.error(request, "Error Updating Course")

    return redirect('admin-dashboard-courses')


# Campus facilities

@login_required(login_url='admin-signin')
def admin_facilities(request):
    facilities_records = CampusFacility.objects.all()
    context = {'segment': 'facilities',
               'facilities_records': facilities_records}
    return render(request, 'project_admin/Campus_facilities.html', context)


@login_required(login_url='admin-signin')
@require_POST
def add_facilities(request):
    name = request.POST['name']
    description = request.POST['description']
    availability = request.POST['availability']
    location = request.POST['location']
    contact_information = request.POST['contact_information']
    hours_of_operation = request.POST['hours_of_operation']

    # Create a new Course object and save it to the database
    campusFacility = CampusFacility(
        name=name,
        availability=availability,
        location=location,
        contact_information=contact_information,
        hours_of_operation=hours_of_operation,
        description=description

    )
    if campusFacility is not None:
        campusFacility.save()
        messages.success(request, 'New facility added successfully.')
    else:
        messages.error(request, 'Error adding facility.')
    return redirect('admin-dashboard-facilities')


@login_required(login_url='admin-signin')
@require_POST
def delete_facility(request, pk):
    # Similar to delete_student function but for Campus_facities model
    facility = get_object_or_404(CampusFacility, campus_facilitiesID=pk)
    facility.delete()
    messages.success(request, "Facility Deleted Successfully")
    return redirect('admin-dashboard-facilities')


@login_required(login_url='admin-signin')
@require_POST
def update_facility(request, facility_id):
    # Retrieve the facility object based on the provided facility_id
    facility = get_object_or_404(
        CampusFacility, campus_facilitiesID=facility_id)
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


# FORMS
@login_required(login_url='admin-signin')
def forms(request):
    context = {'segment': 'forms'}
    return render(request, 'project_admin/forms.html', context)


@login_required(login_url='admin-signin')
def manage_forms(request, category):
    form_category = FormCategory.objects.get(category=category)
    forms = Form.objects.filter(categoryID=form_category)
    # Fetch all campus facilities from the database
    campus_facilities = CampusFacility.objects.all()
    instructors = Instructor.objects.all()
    courses = Course.objects.all()
    # Get the search query from the URL parameters
    query = request.GET.get('query', '')
    if query:
        if form_category.category == 'instructors':
            instructors = instructors.filter(
                Q(first_name__icontains=query) | Q(
                    last_name__icontains=query) | Q(department__icontains=query)
            )
        elif form_category.category == 'courses':
            courses = courses.filter(
                Q(course_name__icontains=query) | Q(
                    course_code__icontains=query) | Q(department__icontains=query)
            )

    if request.method == 'POST':
        form_title = request.POST['form_title']
        if form_title == '':
            messages.error(request, "Please Type a Title")
            return redirect('manage_forms', form_category)
        elif form_category.category == 'facilities':
            selected_facility_id = request.POST['facility']
            try:
                selected_facility = CampusFacility.objects.get(
                    campus_facilitiesID=selected_facility_id)
            except Exception as e:
                messages.error(request, "Please Select a Facility")
                return redirect('manage_forms', form_category)
            form = Form.objects.create(
                title=form_title, categoryID=form_category, content_object=selected_facility)
        elif form_category.category == 'instructors':
            selected_instructor_id = request.POST['instructor']
            try:
                selected_instructor = Instructor.objects.get(
                    instructor_id=selected_instructor_id)
            except Exception as e:
                messages.error(request, "Please Select an Instructor")
                return redirect('manage_forms', form_category)
            form = Form.objects.create(
                title=form_title, categoryID=form_category, content_object=selected_instructor)
        else:
            selected_course_id = request.POST['course']
            try:
                selected_course = Course.objects.get(
                    course_id=selected_course_id)
            except Exception as e:
                messages.error(request, "Please Select a Course")
                return redirect('manage_forms', form_category)
            form = Form.objects.create(
                title=form_title, categoryID=form_category, content_object=selected_course)

            # request.session['current_form_id'] = form.id  # Store the current form ID in the session for later use
        return redirect('add_question', form_category, form.id)

    context = {
        'form_category': form_category.category,
        'campus_facilities': campus_facilities,
        'instructors': instructors,
        'courses': courses,
        'forms': forms,
        'search_query': query,
        'segment': 'forms'
    }

    return render(request, 'project_admin/create_form.html', context)


@login_required(login_url='admin-signin')
def view_form(request, category, form_id):
    try:
        form = Form.objects.get(id=form_id)
        print(form)
        print(category)
        questions = Question.objects.filter(form=form)
        form_category = FormCategory.objects.get(category=category)
        print(form_category.category)
        for question in questions:
            if question.question_type == 'multipleChoice':

                # Convert the 'options' string to a Python object
                options = eval(question.options)
                question.options = options
        context = {
            'form': form, 'questions': questions, 'category': form_category.category, 'segment': 'forms'
        }
        return render(request, 'project_admin/view_form.html', context)
    except Form.DoesNotExist:
        return redirect('admin_dashboard_forms')

# create form


@login_required(login_url='admin-signin')
def create_form(request):
    if request.method == 'POST':
        form_title = request.POST['form_title']
        form = Form.objects.create(title=form_title)
        # request.session['current_form_id'] = form.id  # Store the current form ID in the session for later use
        return redirect('add_question', form.id)

    return render(request, 'project_admin/create_form.html')


# delete form
@login_required(login_url='admin-signin')
@require_POST
def delete_form(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
    print("I am here")
    form.responses.all().delete()
    form.delete()
    print("I am here 2")
    messages.success(request, "Form Deleted Successfully")
    return redirect('admin_dashboard_forms')

# add question


@login_required(login_url='admin-signin')
def add_question(request, category, form_id):
    try:
        form = Form.objects.get(id=form_id)
    except Form.DoesNotExist:
        return redirect('create_form')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_data = form.cleaned_data
            question_data['form'] = form
            Question.objects.create(**question_data)
            return redirect('add_question', form_id=form_id)

    questions = Question.objects.filter(form=form)
    return render(request, 'project_admin/feedback.html', {'form': form, 'questions': questions, 'segment': 'forms'})

# save form


def extract_values_from_options(options):
    values = []
    for option in options:
        # Remove the 'Options: ' prefix
        option = option.replace('Options: ', '')
        # Convert the remaining string to an integer
        value = option.strip()
        values.append(value)
    return values


@login_required(login_url='admin-signin')
def save_form(request, form_id):
    try:
        form = Form.objects.get(id=form_id)
        questions = Question.objects.filter(form=form)
        print(form)
        print(request.POST.get('questionsData', None))
        if request.method == 'POST':
            questions_data = request.POST.get('questionsData', None)
            if questions_data:
                questions_data = json.loads(questions_data)
                for question_data in questions_data:
                    question = Question(
                        form=form,
                        question=question_data['question'],
                        question_type=question_data['questionType']
                    )
                    question.save()
                    if question_data['questionType'] == 'multipleChoice':
                        options = question_data.get('options', '')
                        options = extract_values_from_options(options)
                        print(options)
                        question.options = options
                        question.save()

                messages.success(request, 'New Form created successfully.')
                return redirect('admin_dashboard_forms')

        # Redirect to a new form creation page if not an AJAX POST request
        return redirect('create_form')

    except Form.DoesNotExist:
        return redirect('create_form')


# view form
@login_required(login_url='admin-signin')
def view_form(request, category, form_id):
    try:
        form = Form.objects.get(id=form_id)
        print(form)
        print(category)
        questions = Question.objects.filter(form=form)
        form_category = FormCategory.objects.get(category=category)
        print(form_category.category)
        for question in questions:
            if question.question_type == 'multipleChoice':

                # Convert the 'options' string to a Python object
                options = eval(question.options)
                question.options = options
        context = {
            'form': form, 'questions': questions, 'category': form_category.category, 'segment': 'forms'
        }
        return render(request, 'project_admin/view_form.html', context)
    except Form.DoesNotExist:
        return redirect('admin_dashboard_forms')


@login_required(login_url='admin-signin')
def view_summary_data(request, form_id):
    try:
        form = Form.objects.get(id=form_id)
        questions = Question.objects.filter(form=form)
        all_responses = StudentResponse.objects.filter(form=form)
        visualization_type = request.GET.get(
            'visualization_type', 'bar')  # Default to bar graph

        # Convert all_responses to a pandas DataFrame
        response_data = []
        for response in all_responses:
            response_data.append({
                'student_ID': response.student_ID,
                'question': response.question.question,
                'response_text': response.response_text,
                'response_choice': response.response_choice,
            })
        df = pd.DataFrame(response_data)
        

        try:
            # Create separate dataframes for text-based and option-based responses
            text_responses = df.pivot(
                index='student_ID', columns='question', values='response_text')
            option_responses = df.pivot(
                index='student_ID', columns='question', values='response_choice')

            # Export CSV if 'export' parameter is present in the request
            if 'export' in request.GET and request.GET['export'] == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{form.title}_responses.csv"'
                writer = csv.writer(response)

                # Write the questions with text responses and their corresponding responses
                text_questions = [
                    question.question for question in questions if question.question in text_responses.columns]
                writer.writerow(['Student ID'] + text_questions)
                for student_id, row in text_responses.iterrows():
                    response_row = [
                        row[question] if question in row else '' for question in text_questions]
                    writer.writerow([student_id] + response_row)

                # Write the questions with option responses and their corresponding responses
                option_questions = [
                    question.question for question in questions if question.question in option_responses.columns]
                writer.writerow(['Student ID'] + option_questions)
                for student_id, row in option_responses.iterrows():
                    response_row = [
                        row[question] if question in row else '' for question in option_questions]
                    writer.writerow([student_id] + response_row)

                return response
        except Exception as e:
            has_responses = False 

        # Generate data visualizations based on the selected type
        has_responses = False  # Initialize flag to check if there are responses
        if len(response_data) > 0:
            has_responses = True  # Set flag to True if there are responses
            for question in questions.filter(question_type='multipleChoice'):
                plt.figure(figsize=(8, 6))
                # plt.title(question.question)

                if visualization_type == 'bar':
                    sns.countplot(data=df[df['question'] ==
                                  question.question], x='response_choice')
                    plt.xticks(rotation=45)
                elif visualization_type == 'pie':
                    counts = df[df['question'] ==
                                question.question]['response_choice'].value_counts()
                    plt.pie(counts, labels=counts.index,
                            autopct='%1.1f%%', startangle=140)

                plt.tight_layout()
                plt.savefig(
                    f'static/{form.id}_question_{question.id}_visualization.png')
                plt.close()

        # Render the template for the summary data page
        return render(request, 'project_admin/view_summary_data.html', {
            'form': form,
            'questions': questions,
            'all_responses': all_responses,
            'has_responses': has_responses,  # Pass the flag to the template
            'segment': 'forms'
        })
    except Form.DoesNotExist:
        return redirect('admin_dashboard_forms')

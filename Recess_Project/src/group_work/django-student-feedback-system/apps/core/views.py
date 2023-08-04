from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Student, Course,Campus_facilities,Instructor
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
    # Get the total number of Instructor records in the database
    total_instructors = Instructor.objects.all().count()

    context = {
        'segment': 'index',
        'total_students': total_students,  # Add the count to the context
        'total_instructors': total_instructors,
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

                # --=========================--
                #           Instructors 
                # --=======================---


@login_required(login_url='admin-signin')
def admin_instructors(request):

    instructor_records = Instructor.objects.all()
    context = {'segment': 'instructors', 'instructor_records': instructor_records}

    return render(request, 'project_admin/instructors.html', context)

# Add Instructor to the database

@login_required(login_url='admin-signin')
@require_POST
def add_instructor(request):
    first_name = request.POST['new_first_name']
    instructor_id = request.POST['new_instructor_id']
    last_name = request.POST['new_last_name']
    email = request.POST['new_email']
    department = request.POST['new_department']

    # Validate the uniqueness of the email
    if Instructor.objects.filter(email=email).exists():
        messages.error(request, 'Email address is already in use.')
        return redirect('admin-dashboard-instructors')
    
    # Validate the uniqueness of the instructor_id
    if Instructor.objects.filter(instructor_id=instructor_id).exists():
        messages.error(request, 'Instructor Id already in use')
        return redirect('admin-dashboard-instructors') 

    # Create a new Instructor object and save it to the database
    instructor = Instructor(
        instructor_id=instructor_id,
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
        messages.success(request, "Student Update Successfully")
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


# FORMS

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
    print(query)
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
        if form_category.category == 'facilities':
            selected_facility_id = request.POST['facility']
            selected_facility = CampusFacility.objects.get(
                facility_id=selected_facility_id)

            form = Form.objects.create(
                title=form_title, categoryID=form_category, content_object=selected_facility)
        elif form_category.category == 'instructors':
            selected_instructor_id = request.POST['instructor']
            selected_instructor = Instructor.objects.get(
                instructor_id=selected_instructor_id)
            form = Form.objects.create(
                title=form_title, categoryID=form_category, content_object=selected_instructor)
        else:
            selected_course_id = request.POST['course']
            selected_course = Course.objects.get(
                course_id=selected_course_id)

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
    }

    return render(request, 'project_admin/create_form.html', context)

@login_required(login_url='admin-signin')
def view_all_forms(request):
    forms = Form.objects.all()
    return render(request, 'project_admin/view_all_forms.html', {'forms': forms})




# views.py

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
            'form': form, 'questions': questions, 'category': form_category.category
        }
        return render(request, 'project_admin/view_form.html', context)
    except Form.DoesNotExist:
        return redirect('view_all_forms')

#create form

def create_form(request):
    if request.method == 'POST':
        form_title = request.POST['form_title']
        form = Form.objects.create(title=form_title)
        # request.session['current_form_id'] = form.id  # Store the current form ID in the session for later use
        return redirect('add_question', form.id)

    return render(request, 'project_admin/create_form.html')

#add question
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
    return render(request, 'project_admin/feedback.html', {'form': form, 'questions': questions})

# save form

def extract_values_from_options(options):
    numbers = []
    for option in options:
        # Remove the 'Options: ' prefix
        option = option.replace('Options: ', '')
        # Convert the remaining string to an integer
        number = int(option.strip())
        numbers.append(number)
    return numbers

@login_required(login_url='admin-signin')
@csrf_exempt
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

                return JsonResponse({'message': 'Form data saved successfully'})

        # Redirect to a new form creation page if not an AJAX POST request
        return redirect('create_form')

    except Form.DoesNotExist:
        return redirect('create_form')


#view form
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
            'form': form, 'questions': questions, 'category': form_category.category
        }
        return render(request, 'project_admin/view_form.html', context)
    except Form.DoesNotExist:
        return redirect('view_all_forms')

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
                'student_name': response.student_name,
                'question': response.question.question,
                'response_text': response.response_text,
                'response_choice': response.response_choice,
            })
        print(response_data)
        df = pd.DataFrame(response_data)

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
        })
    except Form.DoesNotExist:
        return redirect('view_all_forms')








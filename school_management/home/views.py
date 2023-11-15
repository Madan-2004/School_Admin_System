from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Student,Employee,FeeDetails,Classwise_Fee,Transportation,FeeRecord,ExpenditureRecord,Cocurriculars,Cocurricular_performance,AcademicGrades
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login as auth_login ,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == "POST":
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_active and role == 'admin':
            auth_login(request,user)
            return render(request,'admin_interface.html')
        else:
            return render(request,'login.html',{'message':'Invalid Credentials !!'})
    return render(request,'login.html')

# def admission(request):
#     return render(request,'admission.html')
def logout(request):
    auth_logout(request)
    return render(request,'index.html')

def academics(request):
    return render(request,'academics.html')

def life(request):
    return render(request,'life.html')

# def about(request):
#     return render(request,'about.html')

# @login_required
def entry(request):
    return render(request,'entry.html')

# @login_required
def student_management(request):
    return render(request,'student_management.html')

@login_required
def employee_management(request):
    return render(request,'employee_management.html')

# @login_required
def finance(request):
    return render(request,'finance.html')

# @login_required
def admin_interface(request):
    return render(request,'admin_interface.html')

@login_required
def new_student(request):
    # student_details={}
    # message = ''
    if request.method == 'POST':
       
        adm_no = request.POST.get('adm_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        aadhar = request.POST.get('aadhar')
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')
        mother_tongue = request.POST.get('mother_tongue')
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        try:
            student = Student.objects.create(
                adm_no=adm_no,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                aadhar=aadhar,
                student_class=student_class,
                section=section,
                mother_tongue=mother_tongue,
                father_name=father_name,
                father_occupation=father_occupation,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                contact=contact,
                address=address
            )
    
            student.save()
    
            # student_details = {
            #     'adm_no': adm_no,
            #     'first_name': first_name,
            #     'last_name': last_name,
            #     'gender': gender,
            #     'dob': dob,
            #     'aadhar': aadhar,
            #     'student_class': student_class,
            #     'section': section,
            #     'mother_tongue': mother_tongue,
            #     'father_name': father_name,
            #     'father_occupation': father_occupation,
            #     'mother_name': mother_name,
            #     'mother_occupation': mother_occupation,
            #     'contact': contact,
            #     'address': address,
            # }

            messages.success(request,"Student Enrolled Successfully")

        except Exception as e:
            messages.error(request,"Please check the Admission No. and other required details")

        return render(request,'student_management.html')
    return render(request,'student_management.html')
    
@login_required
def academic_grades(request):
    if request.method == 'POST':
        adm_no = request.POST.get('adm_no')
        academic_year = request.POST.get('academic_year')
        first_language = request.POST.get('first_language')
        second_language = request.POST.get('second_language')
        third_language = request.POST.get('third_language')
        mathematics = request.POST.get('mathematics')
        science = request.POST.get('science')
        social = request.POST.get('social')
        computers = request.POST.get('computers')
        overall_grade = request.POST.get('overall_grade')

        try:
            student = Student.objects.get(adm_no=adm_no)

            data = AcademicGrades.objects.create(
                adm_no = student,
                student_name = f"{student.first_name} {student.last_name}",
                student_class = student.student_class,
                section = student.section,
                academic_year = academic_year,
                first_language=first_language,
                second_language=second_language,
                third_language=third_language,
                mathematics=mathematics,
                science=science,
                social=social,
                computers=computers,
                overall_grade=overall_grade
            )
            data.save()

            messages.success(request,"Successfull !")
        except Student.DoesNotExist:
            messages.error(request,"Admission No. doesn't exist")
            render(request,'student_management.html')
    return render(request,'student_management.html')

@login_required
def fee(request):

    if request.method == "POST":
        form_type = request.POST.get('form_type')
    
        if form_type == 'fetch':
            
            adm_no = request.POST.get('adm_no')
            student_class = request.POST.get('student_class')

            request.session['adm_no'] = adm_no
            request.session['student_class'] = student_class

            try:
                student = Student.objects.get(adm_no=adm_no)
                student_name = f"{student.first_name} {student.last_name}"
                section = student.section

                request.session['student_name']=student_name
                request.session['section']=section

            except Student.DoesNotExist:
                messages.error(request, "Admission No. doesn't exists")
                return render(request, 'student_management.html')
            
            try:
                class_fee = Classwise_Fee.objects.get(student_class=student_class)

                # student_name = f"{student.first_name} {student.last_name}"
                student_class= class_fee
                tuition_fee = class_fee.tuition_fee
                exam_fee = class_fee.exam_fee
                miscellaneous_fee = class_fee.miscellaneous_fee
    
                fetch_details = {
                    'student_name': student_name,
                    'student_class': student_class,
                    'tuition_fee': tuition_fee,
                    'exam_fee': exam_fee,
                    'miscellaneous_fee': miscellaneous_fee,
                }
    
                return render(request,'student_management.html',{'fetch_details': fetch_details})
            except Classwise_Fee.DoesNotExist:
                messages.error(request,"Admission No. doesn't exists")
                return render(request,'student_management.html')
        
        if form_type == 'fill':
            print("Hello")
            adm_no = request.session.get('adm_no')
            student_class = request.session.get('student_class')
            student_name = request.session.get('student_name')
            section = request.session.get('section')
            area_id = request.POST.get('area_id')
            fee_concession = request.POST.get('fee_concession')
            fee_paid = request.POST.get('fee_paid')
            total_fee = request.POST.get('total_fee')
            balance_fee = request.POST.get('balance_fee')
            try:
                try:

                    student_fee = FeeDetails.objects.get(adm_no=adm_no)
                    student_fee.student_name = student_name
                    student_fee.section = section
                    student_fee.fee_paid = int(student_fee.fee_paid) + int(fee_paid)
                    student_fee.total_fee = int(student_fee.total_fee) + int(total_fee)
                    student_fee.balance_fee = int(student_fee.balance_fee) + int(balance_fee)
                    student_fee.save()
                    messages.success(request,"Updated Successfully")

                except FeeDetails.DoesNotExist:
                    student = Student.objects.get(adm_no=adm_no)
                    class_fee = Classwise_Fee.objects.get(student_class=student_class)
                    transport_area_fee = Transportation.objects.get(area_id=area_id)
                    
                    student_fee = FeeDetails(
                        adm_no=student,
                        student_name = student_name,
                        section = section,
                        student_class=class_fee,
                        area_id=transport_area_fee,
                        transport_fee=transport_area_fee.transport_fee,
                        tuition_fee=0,
                        exam_fee=0,
                        miscellaneous_fee=0,
                        fee_concession=fee_concession,
                        fee_paid=fee_paid,
                        total_fee=total_fee,
                        balance_fee=balance_fee
                    )
                    student_fee.save()
                    messages.success(request,"Saved Successfully")
            except Exception as e:
                messages.error(request,"Please check the Details")
            
            return render(request, 'student_management.html')

    return render(request,'student_management.html')

@login_required
def new_employee(request):

    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        work_type = request.POST.get('work_type')
        working_hours = request.POST.get('working_hours')
        subject_id = request.POST.get('subject_id')
        subject = request.POST.get('subject')
        role = request.POST.get('role')
        account_no = request.POST.get('account_no')
        bank = request.POST.get('bank')
        ifsc_code = request.POST.get('ifsc_code')
        salary = request.POST.get('salary')

        try:
            employee = Employee.objects.create(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                qualification=qualification,
                experience=experience,
                email=email,
                contact=contact,
                work_type=work_type,
                working_hours=working_hours,
                subject_id=subject_id,
                subject=subject,
                role=role,
                account_no=account_no,
                bank=bank,
                ifsc_code=ifsc_code,
                salary=salary
            )
            employee.save()
            messages.success(request,"Employee Added Succesfully")
        except Exception as e:
            messages.error(request,"Please Check the Employee Id and other details !!")
        return render(request,'employee_management.html')

    return render(request,'employee_management.html')

@login_required
def defaults(request):
    return render(request,'defaults.html')

@login_required
def transport(request):
    if request.method == "POST":
        area_id =request.POST.get('area_id')
        area_name = request.POST.get('area_name')
        transport_fee =request.POST.get('transport_fee')

        try:
            area = Transportation.objects.create(
                area_id = area_id,
                area_name = area_name,
                transport_fee = transport_fee
            )
            area.save()

            messages.success(request,"Action Succesfull !")
        except Exception as e:
            messages.error(request,"Sorry! Specifications under this Area Id has already been set")
    return render(request,'defaults.html')

@login_required
def classwise_fee(request):
    if request.method == "POST":
        student_class = request.POST.get('student_class')
        tuition_fee = request.POST.get('tuition_fee')
        exam_fee = request.POST.get('exam_fee')
        miscellaneous_fee = request.POST.get('miscellaneous_fee')

        try:

            classwise_fee_detail = Classwise_Fee.objects.create(
                student_class = student_class,
                tuition_fee = tuition_fee,
                exam_fee = exam_fee,
                miscellaneous_fee = miscellaneous_fee
            )
            classwise_fee_detail.save()

            messages.success(request,"Action Succesfull !")
        except Exception as e:
            messages.error(request,"Sorry ! Specifications for this class has already been set.")

    return render(request,'defaults.html')

@login_required
def view(request):
    entries = Student.objects.all()
    return render(request,'view.html',{'entries':entries})

@login_required
def classwise_students(request):
    if request.method == "POST":
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')

    class_list = Student.objects.filter(student_class=student_class,section=section)

    # for student in class_list:
    #     print(student.first_name)
    return render(request,'view.html',{'list':class_list})

@login_required
def get_student_details(request):
    if request.method == "POST":
        adm_no = request.POST.get('adm_no')

        try:
            student = Student.objects.get(adm_no=adm_no)
            return render(request, 'view.html', {'student': student})
        except Student.DoesNotExist:
            messages.error(request,"Admission No. doesn't exist")
            return render(request, 'view.html')
    
    return render(request, 'view.html')

@login_required
def get_employee_details(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')

        if employee_id:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                return render(request, 'view.html', {'employee': employee})
            except Employee.DoesNotExist:
                messages.error(request,"Employee Id doesn't exist")
                return render(request, 'view.html')

    return render(request, 'view.html')

@login_required
def today_fee_record(request):

    if request.method == "POST":
        
        form_type = request.POST.get('form_type')

        if form_type == 'fetch':
            # print("Hello")
            receipt_no = request.POST.get('receipt_no')
            date = request.POST.get('date')
            adm_no = request.POST.get('adm_no')
            student_class =request.POST.get('student_class')
            section = request.POST.get('section')

            try:
                student = FeeDetails.objects.get(adm_no=adm_no)

            except Exception as e:
                messages.error(request,'Invalid Admission Np. !')
                return render(request,'finance.html')
            
            try:
                student_name = student.student_name
                total_fee = student.total_fee
                balance_fee = student.balance_fee

                request.session['date']=date
                request.session['student_name'] = student_name
                request.session['total_fee'] = str(total_fee)
                request.session['balance_fee'] = str(balance_fee)

                fetch_details = {
                    'student_name': student_name,
                    'total_fee': total_fee,
                    'balance_fee': balance_fee
                }

                return render(request, 'finance.html', {'fetch_details': fetch_details})

            except FeeDetails.DoesNotExist:
                messages.error(request, "Admission No. doesn't exists")
                return render(request, 'finance.html')

        if form_type == 'fill':
            # print("Hello")
            date = request.session.get('date') 
            adm_no = request.session.get('adm_no')
            receipt_no = request.session.get('receipt_no')
            section = request.session.get('section')
            student_class = request.session.get('student_class')
            student_name = request.session.get('student_name')
            balance_fee = request.session.get('balance_fee')
            total_fee = request.session.get('total_fee')

            fee_paid = request.POST.get('fee_paid')

            
            try:
                fee_details = FeeDetails.objects.get(adm_no=adm_no)
                data = FeeRecord.objects.create(
                    date=date,
                    adm_no=fee_details,
                    receipt_no=receipt_no,
                    section=section,
                    student_class=student_class,
                    student_name=student_name,
                    fee_paid=fee_paid,
                    total_fee=total_fee,
                    balance_fee=balance_fee
                )
                data.save()
                messages.success(request, "Done!")
            except FeeDetails.DoesNotExist:
                messages.error(request, "Invalid Details !!")
            
            return render(request, 'finance.html')

    return render(request,'finance.html')

@login_required
def today_expenditure(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')

        # Save the data to the ExpenditureRecord model
        expenditure_record = ExpenditureRecord(
            date=date,
            purpose=purpose,
            amount=amount
        )
        expenditure_record.save()
        messages.success(request,"Added Succesfully !")
        return render(request,'finance.html')
    return render(request,'finance.html')

@login_required
def past_fee_records(request):
    if request.method == "POST":
        date = request.POST.get('date')


        fee_record = FeeRecord.objects.filter(date=date)
        if fee_record:
            return render(request, 'view.html', {'fee_record': fee_record})
        else:
            messages.error("No Record found!")
    return render(request,'view.html')

@login_required
def past_expenditure_records(request):
    if request.method == "POST":
        date = request.POST.get('date')

        expenditure_record = ExpenditureRecord.objects.filter(date=date)
        if expenditure_record:
            return render(request, 'view.html', {'expenditure_record': expenditure_record})
        else:
            messages.error(request,"No Record found !")
            return render(request,'view.html')
    return render(request,'view.html')                                      

@login_required
def activities(request):
    if request.method == "POST":
        activity_id = request.POST.get('activity_id')
        activity_name = request.POST.get('activity_name')

        try:
            entry = Cocurriculars.objects.create(
                activity_id = activity_id,
                activity_name =activity_name
            )
            entry.save()
            messages.success(request,"Action Succesfull !")
        except Exception as e:
            messages.error(request,"Sorry! The Id has already been taken")
    return render(request,'defaults.html')

@login_required
def cocurricular_performance(request):

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'fetch':
            adm_no = request.POST.get('adm_no')
            
            request.session['adm_no']=adm_no

            try:
                student = Student.objects.get(adm_no=adm_no)
                
            except Student.DoesNotExist:
                messages.error(request, "Admission No. doesn't exists")
                return render(request, 'student_management.html')
            
            details_for_cc = {
                'student_name' : f"{student.first_name} {student.last_name}",
                'student_class': student.student_class,
                'section':student.section,
            }

            return render(request,'student_management.html',{'details_for_cc':details_for_cc})
    
        if form_type == 'fill':
           adm_no = request.session.get('adm_no')
           student = Student.objects.get(adm_no=adm_no)
           activity_id = request.POST.get('activity_id')
           performance_remark = request.POST.get('performance_remark')

           activity = Cocurriculars.objects.get(activity_id=activity_id)
           
           entry = Cocurricular_performance.objects.create(
               adm_no = student,
               student_name = f"{student.first_name} {student.last_name}",
               student_class = student.student_class,
               section = student.section,
               activity_id = activity,
               activity_name = activity.activity_name,
               performance_remark = performance_remark
           )

           entry.save()
           messages.success(request,"Successfull !")
           return render(request,'student_management.html')
    return render(request,'student_management.html')

@login_required
def modify_employee_details(request):
    
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'fetch':
            employee_id = request.POST.get('employee_id')
            
            request.session['employee_id']=employee_id

            try:
                employee = Employee.objects.get(employee_id=employee_id)
            except Exception as e:
                messages.error(request,'Invalid Employee ID')
                return render(request,'employee_management.html')
            
            try:
                first_name = employee.first_name
                last_name = employee.last_name
                qualification = employee.qualification
                experience= employee.experience
                email = employee.email
                contact = employee.contact

                fetch_details = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'qualification': qualification,
                    'experience': experience,
                    'email': email,
                    'contact': contact
                }

                return render(request,'employee_management.html',{'fetch_details': fetch_details})
            
            except Employee.DoesNotExist:
                messages.error(request,"Invalid Employee ID")
                return render(request,'employee_management.html')
            
        if form_type == 'fill':

            employee_id = request.session.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            qualification = request.POST.get('qualification')
            experience = request.POST.get('experience')
            email = request.POST.get('email')
            contact = request.POST.get('contact')

            try:
                try:
                    employee = Employee.objects.get(employee_id=employee_id)

                    if first_name:
                        employee.first_name = first_name
                    if last_name:
                        employee.last_name = last_name
                    if qualification:
                        employee.qualification = qualification
                    if experience:
                        employee.experience = experience
                    if email:
                        employee.email = email
                    if contact:
                        employee.contact = contact

                    employee.save()
                    messages.success(request,"Updated Succesfully")
                    
                except Employee.DoesNotExist :
                    try:
                        entry = Employee(
                            employee_id=employee_id,
                            first_name=first_name,
                            last_name=last_name,
                            qualification=qualification,
                            experience=experience,
                            email=email,
                            contact=contact
                        )
                        entry.save()
                        messages.success(request, "No Modifications Made!")
                    except Exception as e:
                        messages.error(request, "Invalid Employee Id")
            except Exception as e:
                messages.error(request,"Invalid Employee Id")
            
            return render(request,'employee_management.html')

    return render(request,'employee_management.html')

@login_required
def modify_work_details(request):

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'fetch':
            employee_id = request.POST.get('employee_id')
            
            request.session['employee_id']=employee_id

            try:
                employee = Employee.objects.get(employee_id=employee_id)
            except Exception as e:
                messages.error(request,'Invalid Employee ID')
                return render(request,'employee_management.html')
            
            try:
                first_name = employee.first_name
                last_name = employee.last_name
                work_type = employee.work_type
                working_hours = employee.working_hours
                subject_id = employee.subject_id
                subject= employee.subject
                role = employee.role

                details = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'work_type': work_type,
                    'working_hours': working_hours,
                    'subject_id': subject_id,
                    'subject': subject,
                    'role':role
                }

                return render(request,'employee_management.html',{'details': details})
            
            except Employee.DoesNotExist:
                messages.error(request,"Invalid Employee ID")
                return render(request,'employee_management.html')

        if form_type == 'fill':
            employee_id = request.session.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            work_type = request.POST.get('work_type')
            working_hours = request.POST.get('working_hours')
            subject_id = request.POST.get('subject_id')
            subject = request.POST.get('subject')
            role = request.POST.get('role')

            try:
                try:
                    employee = Employee.objects.get(employee_id=employee_id)

                    if first_name:
                        employee.first_name = first_name
                    if last_name:
                        employee.last_name = last_name
                    if work_type:
                        employee.work_type = work_type
                    if working_hours:
                        employee.working_hours = working_hours
                    if subject_id:
                        employee.subject_id = subject_id
                    if subject:
                        employee.subject = subject
                    if working_hours:
                        employee.working_hours = working_hours
                    if role:
                        employee.role = role

                    employee.save()
                    messages.success(request, "Updated Successfully")
                    
                except Employee.DoesNotExist:
                    try:
                        entry = Employee(
                            employee_id=employee_id,
                            first_name=first_name,
                            last_name=last_name,
                            work_type=work_type,
                            working_hours=working_hours,
                            subject_id=subject_id,
                            subject=subject,
                            role=role
                        )
                        entry.save()
                        messages.success(request, "No Modifications Made!")
                    except Exception as e:
                        messages.error(request, "Invalid Employee Id")
            except Exception as e:
                messages.error(request, "Invalid Employee Id")

            return render(request, 'employee_management.html')

    return render(request, 'employee_management.html')

@login_required
def modify_salary_details(request):
    
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        
        if form_type == 'fetch':
            employee_id = request.POST.get('employee_id')
            
            request.session['employee_id']=employee_id

            try:
                employee = Employee.objects.get(employee_id=employee_id)
            except Exception as e:
                messages.error(request,'Invalid Employee ID')
                return render(request,'employee_management.html')
            
            try:
                first_name = employee.first_name
                last_name = employee.last_name
                account_no = employee.account_no
                bank= employee.bank
                ifsc_code = employee.ifsc_code
                salary = employee.salary

                salary_details = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'account_no': account_no ,
                    'bank': bank,
                    'ifsc_code': ifsc_code,
                    'salary': salary
                }

                return render(request,'employee_management.html',{'salary_details': salary_details})
            
            except Employee.DoesNotExist:
                messages.error(request,"Invalid Employee ID")
                return render(request,'employee_management.html')
            
        if form_type == 'fill':
            employee_id = request.session.get('employee_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            account_no = request.POST.get('account_no')
            bank = request.POST.get('bank')
            ifsc_code = request.POST.get('ifsc_code')
            salary= request.POST.get('salary')

            try:
                try:
                    employee = Employee.objects.get(employee_id=employee_id)

                    if first_name:
                        employee.first_name = first_name
                    if last_name:
                        employee.last_name = last_name
                    if account_no:
                        employee.account_no = account_no
                    if bank:
                        employee.bank = bank
                    if ifsc_code:
                        employee.ifsc_code = ifsc_code
                    if salary:
                        employee.salary = salary

                    employee.save()
                    messages.success(request, "Updated Successfully")
                    
                except Employee.DoesNotExist:
                    try:
                        entry = Employee(
                            employee_id=employee_id,
                            first_name=first_name,
                            last_name=last_name,
                            account_no=account_no,
                            bank=bank,
                            ifsc_code=ifsc_code,
                            salary=salary
                        )
                        entry.save()
                        messages.success(request, "No Modifications Made!")
                    except Exception as e:
                        messages.error(request, "Invalid Employee Id")
            except Exception as e:
                messages.error(request, "Invalid Employee Id")

            return render(request, 'employee_management.html') 

    return render(request,'employee_management.html')

@login_required
def modify_student_details(request):
    if request.method == "POST":
        form_type= request.POST.get('form_type')

        if form_type == "fetch":

            adm_no = request.POST.get('adm_no')

            request.session['adm_no'] = adm_no

            try:
                student = Student.objects.get(adm_no=adm_no)
            except Student.DoesNotExist:
                messages.error(request, "Invalid Admission Number")
                return render(request, 'student_management.html')
            
            try:
                first_name = student.first_name
                last_name = student.last_name
                gender = student.gender
                dob = student.dob
                aadhar = student.aadhar
                student_class = student.student_class
                section = student.section
                mother_tongue = student.mother_tongue
                father_name = student.father_name
                father_occupation = student.father_occupation
                mother_name = student.mother_name
                mother_occupation = student.mother_occupation
                contact = student.contact
                address = student.address

                student_details = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'dob': dob,
                    'aadhar': aadhar,
                    'student_class': student_class,
                    'section': section,
                    'mother_tongue': mother_tongue,
                    'father_name': father_name,
                    'father_occupation': father_occupation,
                    'mother_name': mother_name,
                    'mother_occupation': mother_occupation,
                    'contact': contact,
                    'address': address
                }

                return render(request, 'student_management.html', {'student_details': student_details})
            except Student.DoesNotExist:
                messages.error(request, "Invalid Admission Number")
                return render(request, 'student_management.html')
        
        if form_type == 'fill':
                
                adm_no = request.session.get('adm_no')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                gender = request.POST.get('gender')
                dob = request.POST.get('dob')
                aadhar = request.POST.get('aadhar')
                student_class = request.POST.get('student_class')
                section = request.POST.get('section')
                mother_tongue = request.POST.get('mother_tongue')
                father_name = request.POST.get('father_name')
                father_occupation = request.POST.get('father_occupation')
                mother_name = request.POST.get('mother_name')
                mother_occupation = request.POST.get('mother_occupation')
                contact = request.POST.get('contact')
                address = request.POST.get('address')

                try:
                    try:
                        student = Student.objects.get(adm_no=adm_no)

                        if first_name:
                            student.first_name = first_name
                        if last_name:
                            student.last_name = last_name
                        if gender:
                            student.gender = gender
                        if dob:
                            student.dob = dob
                        if aadhar:
                            student.aadhar = aadhar
                        if student_class:
                            student.student_class = student_class
                        if section:
                            student.section = section
                        if mother_tongue:
                            student.mother_tongue = mother_tongue
                        if father_name:
                            student.father_name = father_name
                        if father_occupation:
                            student.father_occupation = father_occupation
                        if mother_name:
                            student.mother_name = mother_name
                        if mother_occupation:
                            student.mother_occupation = mother_occupation
                        if contact:
                            student.contact = contact
                        if address:
                            student.address = address

                        student.save()
                        messages.success(request, "Updated Successfully")
            
                    except Student.DoesNotExist:
                        try:
                            entry = Student(
                                adm_no=adm_no,
                                first_name=first_name,
                                last_name=last_name,
                                gender=gender,
                                dob=dob,
                                aadhar=aadhar,
                                student_class=student_class,
                                section=section,
                                mother_tongue=mother_tongue,
                                father_name=father_name,
                                father_occupation=father_occupation,
                                mother_name=mother_name,
                                mother_occupation=mother_occupation,
                                contact=contact,
                                address=address
                            )
                            entry.save()
                            messages.success(request, "No Modifications Made!")
                        except Exception as e:
                            messages.error(request, "Invalid Admission Number")
                except Exception as e:
                    messages.error(request, "Invalid Admission Number")

                return render(request, 'student_management.html')

    return render(request, 'student_management.html')

@login_required
def modify_fee(request):
    if request.method == "POST":
        form_type= request.POST.get('form_type')

        if form_type =='fetch':
            student_class = request.POST.get('student_class')
            request.session['student_class']=student_class

            try:
                fee = Classwise_Fee.objects.get(student_class=student_class)
            except Classwise_Fee.DoesNotExist:
                messages.error(request,"Please Select a Valid Class")
                return render(request,'defaults.html')
            try:
                tuition_fee = fee.tuition_fee
                exam_fee = fee.exam_fee
                miscellaneous_fee = fee.miscellaneous_fee

                fee_details = {
                    'student_class': student_class,
                    'tuition_fee': tuition_fee,
                    'exam_fee': exam_fee,
                    'miscellaneous_fee': miscellaneous_fee,
                }

                return render(request, 'defaults.html', {'fee_details': fee_details})
            
            except Classwise_Fee.DoesNotExist:
                messages.error(request, "Classwise fee not found for the selected class")
                return render(request, 'defaults.html')
            
        if form_type == 'fill':
            student_class = request.session.get('student_class')
            tuition_fee = request.POST.get('tuition_fee')
            exam_fee = request.POST.get('exam_fee')
            miscellaneous_fee = request.POST.get('miscellaneous_fee')

            try:
                try:
                    class_fee = Classwise_Fee.objects.get(student_class=student_class)

                    if tuition_fee:
                        class_fee.tuition_fee = tuition_fee
                    if exam_fee:
                        class_fee.exam_fee = exam_fee
                    if miscellaneous_fee:
                        class_fee.miscellaneous_fee = miscellaneous_fee

                    class_fee.save()
                    messages.success(request, "Updated successfully")
                except Classwise_Fee.DoesNotExist:
                    try:
                        entry = Classwise_Fee(
                            student_class=student_class,
                            tuition_fee=tuition_fee,
                            exam_fee=exam_fee,
                            miscellaneous_fee=miscellaneous_fee
                        )
                        entry.save()
                        messages.success(request, "Classwise fee details created successfully")
                    except Exception as e:
                        messages.error(request, "Invalid student class")
            except Exception as e:
                messages.error(request, "Invalid student class")

            return render(request, 'defaults.html')    
    return render(request,'defaults.html')

@login_required
def modify_transport(request):
    if request.method == "POST":
        form_type= request.POST.get('form_type')

        if form_type =='fetch':
            area_id = request.POST.get('area_id')
            request.session['area_id']=area_id

            try:
                area = Transportation.objects.get(area_id=area_id)
            except Exception as e:
                messages.error(request,"Invalid Area Id")
                return render(request,'defaults.html')
            try:
                area_id = area.area_id
                area_name = area.area_name
                transport_fee = area.transport_fee

                area_details ={
                    'area_id':area_id,
                    'area_name':area_name,
                    'transport_fee':transport_fee
                }
                return render(request,'defaults.html',{'area_details':area_details})
            except Transportation.DoesNotExist:
                messages.error(request,"Invalid Area Id")
                return render(request,'defaults.html')
        
        if form_type == 'fill':
            area_id = request.session.get('area_id')
            area_name = request.POST.get('area_name')
            transport_fee = request.POST.get('transport_fee')

            try:
                try:
                    area = Transportation.objects.get(area_id=area_id)

                    if area_name:
                        area.area_name = area_name
                    if transport_fee:
                        area.transport_fee = transport_fee

                    area.save()
                    messages.success(request, "Updated successfully")
                
                except Transportation.DoesNotExist:
                    try:
                        entry = Transportation(
                            area_id=area_id,
                            area_name=area_name,
                            transport_fee=transport_fee
                        )
                        entry.save()
                        messages.success(request, "Transport area details created successfully")
                    except Exception as e:
                        messages.error(request, "Invalid area ID")
            except Exception as e:
                messages.error(request, "Invalid area ID")

            return render(request, 'defaults.html')

        return render(request, 'defaults.html')

    return render(request,'defaults.html')

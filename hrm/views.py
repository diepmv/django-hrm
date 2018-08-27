# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import name
from xml.sax import handler

import hashlib
import os
from  django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import os
import logging

from django.template import context
from django.urls import reverse, reverse_lazy

from django.contrib import messages
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt
from pip.compat import console_to_str

from . import forms
import hashlib
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from . import forms
from .models import *
from datetime import *

# Create your views here.

logging.basicConfig(filename="test.log", level=logging.DEBUG)


def index(request):
    pos = session.query(Position).all()
    context = {'pos': pos}
    template = 'index.html'
    return render(request, template, context)


from .models import Position, session, ResetPassword, Employee, Message, Notification, CreateNewUser, Image


# Create your views here.


# def test(request):
#     a = request.session.get_expire_at_browser_close()
#     form = forms.LoginForm(request.POST)
#
#     return render(request, 'test.html', {'form': form})

def employee_login(request):
    """
    authenticate User
    :param request:
    :return:
    """
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        password = request.POST['password']
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            employee = authenticate(username=username, password=password)

            if employee is not None:
                if employee.is_active:
                    login(request, employee)
                    return JsonResponse("redirect", safe=False)

            else:
                return JsonResponse("wrong", safe=False)

        else:
            return JsonResponse("invalid", safe=False)

    return render(request, 'index.html', {'form': form})


def employee_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse('login'))


@login_required()
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home.html', context)


def restore_pass(request):
    form = forms.EmailForm()
    if request.method == "POST":
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            token = hashlib.sha256(email.encode()).hexdigest()
            reset_pass = ResetPassword(email=email, token=token)
            session.add(reset_pass)
            session.commit()

            url_reset = 'http://localhost:8000' + reverse('create-new-password') + "?token={}".format(token)

            subject = "Reset password instructions"
            message = "Hello {}! Someone has requested a link to change your password. You can do this through the link below. {} ".format(
                email, url_reset)
            send_mail(subject, message, 'admin', [email])

    return render(request, 'forgot_pass.html', {'form': form})


def create_new_password(request):
    """
    create new password when user click confirmation link
    :param request:
    :return:
    """
    if request.method == "GET":
        form = forms.PasswordForm()
        return render(request, 'create_new_password.html', {"form": form})

    elif request.method == "POST":
        form = forms.PasswordForm(request.POST)
        if form.is_valid():
            token = request.GET.get('token', '')
            reset_pass = session.query(ResetPassword).filter_by(token=token).first()
            #number of days from reseting day
            if reset_pass:
                days = (datetime.now() - reset_pass.reset_on).days
                if days >=2:
                    session.delete(reset_pass)
                    session.commit
                    return JsonResponse("expired", safe=False)
                new_password = form.cleaned_data['password']
                email = reset_pass.email
                # employee = session.query(Employee).filter_by(email=email).one()
                employee = session.query(Employee).filter_by(email=email).first()
                employee.password = make_password(new_password)
                session.commit()

                #After reset password successfully, delete token

                session.delete(reset_pass)
                session.commit()

                return JsonResponse("success", safe=False)
            else:
                return JsonResponse("expired", safe=False)
        else:
            return JsonResponse("invalid", safe=False)

    else:
        logging.debug("Invalid method!")




# handle upload avatar => save image to server
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


def handle_uploaded_file(f, filename):
    with open("{}/pic_folder/{}".format(MEDIA_ROOT, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required()
def profile_detail(request):
    update_skill_form = forms.UpdateSkillsForm()
    add_skill_form = forms.AddSkillForm()
    current_user = request.user
    pos_id = current_user.pos_id
    if pos_id:
        pos = session.query(Position).get(pos_id)
        position = pos.name
    else:
        position = None
        pos = None
        logging.debug("Current user have no position in DB")
    relationship_form = forms.RelationshipForm()
    update_edu_form = forms.UpdateEduForm()
    add_edu_form = forms.AddEduForm()
    all_edu = session.query(EmployeeSchoolLink).filter_by(employee_id=current_user.id)
    timestamps = []
    for edu in all_edu:
        timestamps.append(edu.start_date)
        timestamps.append(edu.end_date)
        # timestamps.append(start.strftime('%Y-%m-%d'))
        # timestamps.append(end.strftime('%Y-%m-%d'))
    timestamps = sorted(timestamps)
    print(timestamps)
    context = {'position': pos, 'update_skill_form': update_skill_form,
               'add_skill_form': add_skill_form, 'position': position, "relationship_form": relationship_form,
               'update_edu_form': update_edu_form,
               'add_edu_form': add_edu_form, 'timestamps': timestamps}
    if request.method == 'POST':
        # change info
        if request.POST.get('submit') == 'Update':
            # update image in server db
            if "ava-filechooser" in request.FILES:
                handle_uploaded_file(request.FILES['ava-filechooser'], request.FILES['ava-filechooser'].name)
                if current_user.image_id:  # if user already has ava -> just edit
                    img = session.query(Image).filter_by(id=current_user.image_id).first()
                    img.name = request.FILES['ava-filechooser'].name
                    img.type = request.FILES['ava-filechooser'].content_type
                    img.path = "pic_folder/{}".format(request.FILES['ava-filechooser'].name)
                    session.commit()
                else:  # if user use default ava (image_id = null) -> add image to server db
                    avatar = Image(name=request.FILES['ava-filechooser'].name,
                                   type=request.FILES['ava-filechooser'].content_type,
                                   path="pic_folder/{}".format(request.FILES['ava-filechooser'].name))
                    session.add(avatar)
                    session.commit()
                    current_user.image_id = avatar.id
                    session.commit()
            fullname = request.POST.get('full-name')
            gender = request.POST.get('gender')
            dOB = request.POST.get('dOB')
            if dOB == "":
                dOB = current_user.dob
            username = request.POST.get('username')
            # session.add(Image(name=avatar))
            current_user.name = fullname
            if gender == 'male':
                current_user.gender = 'M'
            if gender == 'female':
                current_user.gender = 'F'
            current_user.dob = dOB
            current_user.username = username
            session.commit()

        ##change pass
        if request.POST.get('submit') == 'Change':
            current_pwd = request.POST.get('old-pass')
            new_pwd = request.POST.get('new-pass1')
            new_pwd_confirm = request.POST.get('new-pass2')
            if current_pwd != current_user.password:
                messages.error(request, 'Wrong current password')
            if new_pwd != new_pwd_confirm:
                messages.warning(request, 'New password did not match')
            current_user.password = new_pwd
            session.commit()
    return render(request, 'profile_detail.html', context)


def reset_pass(request):
    return render(request, 'reset_pass.html')


def subtree(request):
    emps = session.query(Employee).filter_by(parent=1)
    root = session.query(Employee).get(1)
    context = {'instances': emps, 'root': root}
    return render(request, 'subtree.html', context)


def createUser(request):
    """
    Create new employee and notify to employee via email
    :param request:
    :return:
    """
    form = forms.EmailForm()
    if request.method == 'POST':
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            # add email to db
            email = form.cleaned_data['email']
            # check if email exist
            m = session.query(Employee).filter_by(email=email).all()

            if not m:
                object = Employee(email=email, is_active=1)
                session.add(object)
                session.commit()
            else:
                return JsonResponse("exist", safe=False)

            # send email to user
            token = hashlib.sha256(email.encode()).hexdigest()
            create_newuser = CreateNewUser(email=email, token=token)
            session.add(create_newuser)
            session.commit()

            url = 'http://127.0.0.1:8000' + reverse('update-account') + "?token={}".format(token)

            subject = "Update account info"
            message = "Hello {}! Click link below to update your account {}".format(email, url)
            if send_mail(subject, message, 'diepmv.ptit@gmail.com', [email]):
                return JsonResponse("success", safe=False)
            else:
                return JsonResponse("fail", safe=False)

    return render(request, 'create-user.html', {'form': form})


def update_account(request):
    """
    Upadate account after user click to the comfirmmation URL
    :param request:
    :return:
    """
    form = forms.UpdateNewAccountForm()
    if request.method == "GET":
        token = request.GET.get('token', '')

    elif request.method == 'POST':
        form = forms.UpdateNewAccountForm(request.POST)
        if form.is_valid():
            token = request.GET.get('token', '')

            create_new_user = session.query(CreateNewUser).filter_by(token=token).first()
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password'])
            if create_new_user:
                email = create_new_user.email
                employee = session.query(Employee).filter_by(email=email).first()

                if not employee:
                    employee.username = username
                    employee.password = password
                    session.commit()
                    return HttpResponseRedirect(reverse('login'))
                else:
                    logging.debug("Email is not exist in database")

    return render(request, 'update-new-account.html', {"form": form})


# -> Comment ham

@csrf_exempt
def compose(request):
    # Log::debug(request)
    #
    # result = validateParam() : Ko tin vao dk ben ngoai
    # if (result != 0)
    #     return ;

    if request.method == "POST":
        # Log
        print("********************************")
        receivers = request.POST.get('to').split(',')
        m_subject = request.POST.get('subject')
        m_content = request.POST.get('message-content')
        message = Message(subject=m_subject, content=m_content)
        session.add(message)
        session.commit()
        session.refresh(message)
        if 'all' in receivers:
            all_receivers = session.query(Employee).all()
            if request.user in all_receivers:
                all_receivers.remove(request.user)
            # else
            #     Log
            for r in all_receivers:
                # Log::debug(r)
                session.add(Notification(message_id=message.id, user_id=r.id))
                session.commit()

        else:
            for r in receivers:
                receiver = session.query(Employee).filter_by(username=r).one()
                # receiver_id = receiver.id
                # print(receiver_id)
                session.add(Notification(message_id=message.id, user_id=receiver.id))
                session.commit()
                # else
                # Log::
                ##########################################
    return render(request, 'compose_mail.html')


def mailbox(request):
    notifications = session.query(Notification).filter_by(user_id=request.user.id)
    print(type(notifications))
    unseen_nums = session.query(Notification).filter_by(seen=0, user_id=request.user.id).count()
    context = {'notifications': notifications, 'unseen_nums': unseen_nums}
    return render(request, 'mailbox.html', context=context)


def read_mail(request, pk):
    mess = session.query(Message).get(pk)
    noti = session.query(Notification).filter_by(user_id=request.user.id, message_id=pk).one()
    noti.seen = 1
    session.commit()
    context = {'message': mess}


def update_skill(request):
    '''
    usage: update skill date
    :param request:
    :return:
    '''
    form = forms.UpdateSkillsForm(request.POST)
    if form.is_valid():
        id = request.GET.get("id")  # get record id in database
        # get request params
        month_start = request.POST.get('date_start_month')
        day_start = request.POST.get('date_start_day')
        year_start = request.POST.get('date_start_year')
        month_end = request.POST.get('date_end_month')
        day_end = request.POST.get('date_end_day')
        year_end = request.POST.get('date_end_year')
        # update by newest data
        personal_skill = session.query(EmployeeSkillLink).filter_by(id=id).first()
        personal_skill.start_date = year_start + "-" + month_start + "-" + day_start
        personal_skill.end_date = year_end + "-" + month_end + "-" + day_end
        session.commit()  # confirm change
    # else:
    #     form.


    return HttpResponseRedirect(reverse('profile_detail'))


def add_skill(request):
    '''
    usage: add new skill
    :param request:
    :return:
    '''
    form = forms.AddSkillForm(request.POST)
    if form.is_valid():
        current_user = request.user  # get current user
        # get requets params
        skill_add = request.POST.get("skills")
        month_start = request.POST.get('date_start_month')
        day_start = request.POST.get('date_start_day')
        year_start = request.POST.get('date_start_year')
        month_end = request.POST.get('date_end_month')
        day_end = request.POST.get('date_end_day')
        year_end = request.POST.get('date_end_year')
        print("------------------------------------")
        skill = session.query(Skill).filter_by(name=skill_add).one()
        new_skill_start_date = year_start + "-" + month_start + "-" + day_start
        new_skill_end_date = year_end + "-" + month_end + "-" + day_end
        # add new record to employee_skill table
        session.add(EmployeeSkillLink(employee_id=current_user.id, skill_id=skill.id, start_date=new_skill_start_date,
                                      end_date=new_skill_end_date))
        # confirm query
        session.commit()

    return HttpResponseRedirect(reverse('profile_detail'))


def add_relationship(request):
    """
    Adding relationship to current user
    """
    logging.debug("Logging request parameters: name: {}, relationship: {}".format(request.POST.get("name"),
                                                                                  request.POST.get("rela_name")))
    form = forms.RelationshipForm(request.POST)
    if form.is_valid():
        name = request.POST.get("name")
        rela_name = request.POST.get("rela_name")

        relationship = session.query(Relationship).filter_by(name=rela_name).first()
        if relationship is not None:
            relationship_id = relationship.id
            employee_id = request.user.id
            employee_relationship = EmployeeRelationshipLink(employee_id=employee_id, relationship_id=relationship_id,
                                                             name=name)
            session.add(employee_relationship)
            session.commit()
            return HttpResponseRedirect(reverse('profile_detail'))
        else:
            logging.debug("Relationship object:".format(relationship))

    else:
        logging.debug("Invalid form")


def update_relationship(request):
    """
    Update relationship of current User logged-in.
    """
    logging.debug(
        "Logging request parameter: id: {}, name: {}, rela: {}".format(request.GET.get('id'), request.POST['name'],
                                                                       request.POST['rela_name']))

    form = forms.RelationshipForm(request.POST)
    if form.is_valid():
        id = request.GET.get("id")
        name = form.cleaned_data['name']
        rela = form.cleaned_data['rela_name']
        employee_id = request.user.id
        relationship = session.query(Relationship).filter_by(name=rela).first()
        if relationship is not None:
            relationship_id = relationship.id
        else:
            logging.debug("Relationship object: {}".format(relationship))
        employee_relationship = session.query(EmployeeRelationshipLink).get(id)
        employee_relationship.name = name
        employee_relationship.relationship_id = relationship_id
        session.commit()

        return HttpResponseRedirect(reverse("profile_detail"))
    else:
        logging.debug("Invalid form.")


def update_education(request):
    '''
       usage: update edu info
       :param request:
       :return:
       '''
    form = forms.UpdateEduForm(request.POST)
    if form.is_valid():
        id = request.GET.get("id")  # get record id in database
        # get request params
        degree = request.POST.get('degree')
        month_start = request.POST.get('start_month')
        day_start = request.POST.get('start_day')
        year_start = request.POST.get('start_year')
        month_end = request.POST.get('end_month')
        day_end = request.POST.get('end_day')
        year_end = request.POST.get('end_year')
        # update by newest data
        personal_edu = session.query(EmployeeSchoolLink).filter_by(id=id).first()
        personal_edu.degree_type = degree
        personal_edu.start_date = year_start + "-" + month_start + "-" + day_start
        personal_edu.end_date = year_end + "-" + month_end + "-" + day_end
        session.commit()  # confirm change
        # else:
        #     form.
    return HttpResponseRedirect(reverse("profile_detail"))


def add_edu(request):
    '''
    usage: add new edu info
    :param request:
    :return:
    '''
    form = forms.AddEduForm(request.POST)
    if form.is_valid():
        current_user = request.user  # get current user
        # get requets params
        edu_add = request.POST.get("school")
        degree = request.POST.get("degree")
        month_start = request.POST.get('date_start_month')
        day_start = request.POST.get('date_start_day')
        year_start = request.POST.get('date_start_year')
        month_end = request.POST.get('date_end_month')
        day_end = request.POST.get('date_end_day')
        year_end = request.POST.get('date_end_year')
        all_schools = session.query(School).all()
        all_school_names = []
        for s in all_schools:
            all_school_names.append(s.name)
        if edu_add not in all_school_names:
            session.add(School(name=edu_add))
        school = session.query(School).filter_by(name=edu_add).one()
        new_skill_start_date = year_start + "-" + month_start + "-" + day_start
        new_skill_end_date = year_end + "-" + month_end + "-" + day_end
        # add new record to employee_skill table
        session.add(
            EmployeeSchoolLink(employee_id=current_user.id, school_id=school.id, start_date=new_skill_start_date,
                               end_date=new_skill_end_date, degree_type=degree))
        # confirm query
        session.commit()

    return HttpResponseRedirect(reverse('profile_detail'))


def handle_uploaded_document(f, filename):
    with open("{}/documents/{}".format(MEDIA_ROOT, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def add_document(request):
    """
    Add document to current employee
    """
    if request.method == "POST":
        if "document" in request.FILES:
            handle_uploaded_document(request.FILES['document'], request.FILES['document'].name)

            employee_id = request.user.id
            name = request.FILES["document"].name
            type = request.FILES['document'].content_type
            path = "documents/{}".format(request.FILES['document'].name)
            document = Document(employee_id=employee_id, name=name, type=type, path=path)
            session.add(document)
            session.flush()

            session.refresh(document)
            if document.is_image():
                element = '<a href="http://localhost:8025/media/{}" data-lightbox="roadtrip"><img  height="100" width="150" src="http://localhost:8025/media/{}" alt="avatar"></a>'.format(
                    document.path, document.path)
                return JsonResponse({"element": element})

            elif document.is_pdf():
                element = '<a href="http://localhost:8025/media/{}"><img height="100" width="150" src="http://localhost:8025/media/documents/pdf.png" alt="avatar"></a>'.format(
                    document.path)
                return JsonResponse({"element": element})
            else:
                element = '<a href="http://localhost:8025/media/{}"><img height="100" width="150" src="http://localhost:8025/media/documents/doc.jpg" alt="avatar"></a'.format(
                    document.path)
                return JsonResponse({"element": element})

        else:
            logging.debug("there are no file to process")
    else:
        logging.debug("invalid request")

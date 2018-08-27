from django.conf.urls import url

from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.employee_login, name='login'),
    url(r'^logout/$', views.employee_logout, name='logout'),
    url(r'^create_new_password', views.create_new_password , name='create-new-password'),

]

urlpatterns += [
    url(r'^home/$', views.home, name='home'),
    url(r'restore_pass/$', views.restore_pass, name='restore-password'),
    url(r'mailbox/$', views.mailbox, name='mailbox'),

    url(r'profiledetail/$', views.profile_detail, name = 'profile_detail'),
    url(r'compose/$', views.compose, name='compose'),
    url(r'resetpass/$', views.reset_pass, name='reset_pass'),
    url(r'company-hierarchy/$', views.subtree, name='company-hierarchy'),
    url(r'create-user/$', views.createUser, name='create-user'),
    url(r'readmail/(?P<pk>\d+)$', views.read_mail, name='read-mail'),
    url(r'update-account/$', views.update_account, name='update-account'),
    url(r'update-skill/$', views.update_skill, name = 'update-skill'),
    url(r'add-skill/$', views.add_skill, name = 'add-skill'),
    url(r'add-relationship/$', views.add_relationship, name="add-relationship"),
    url(r'update-relationship/$', views.update_relationship, name='update-relationship'),
    url(r'update-edu/$', views.update_education, name = 'update-edu'),
    url(r'add-edu/$', views.add_edu, name="add-edu"),
    url(r'add-document/$', views.add_document, name='add-document'),
]

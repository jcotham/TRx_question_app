
from django.conf.urls import patterns, url

from questions import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^chain/$', views.chain, name='chain'),

    #project/set
    url(r'^addProject/$', views.addProject, name='addProject'),
    url(r'^editProject/(?P<project_index>\d+)/$', views.editProject, name='editProject'),

    #chain
    url(r'^editProject/(?P<project_index>\d+)/addChain/$', views.addChain, name='addChain'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/$', views.editChain, name='editChain'),

    #question
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/$', views.editQuestion, name='editQuestion'),

    #options:
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/addOptions/$', views.addOptions, name='addOptions'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/editOptions/$', views.editOptions, name='editOptions'),



    #url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/$', views.editQuestion, name='editQuestion'),
    #url(r'^addChain/$', views.addChain, name='addChain'),
    #url(r'^(?P<QuestionChain_id>\d+)/edit/$', views.editChain, name='editChain'),
)


from django.conf.urls import patterns, url

from questions import views

urlpatterns = patterns('',
    url(r'^$', views.projectHome, name='projectHome'),
    url(r'^index/$', views.index, name='index'),

    #project/set
    url(r'^addProject/$', views.addProject, name='addProject'),
    url(r'^deleteProject/(?P<project_index>\d+)/$', views.deleteProject, name='deleteProject'),
    url(r'^saveProject/(?P<project_index>\d+)/$', views.saveProject, name='saveProject'),
    url(r'^editProject/(?P<project_index>\d+)/$', views.editProject, name='editProject'),

    #chain
    url(r'^editProject/(?P<project_index>\d+)/addChain/$', views.addChain, name='addChain'),
    url(r'^saveChain/(?P<chain_index>\d+)/$', views.saveChain, name='saveChain'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/$', views.editChain, name='editChain'),

    #question
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/$', views.editQuestion, name='editQuestion'),

    #options:
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/addOptions/$', views.addOptions, name='addOptions'),
    url(r'^editProject/(?P<project_index>\d+)/editChain/(?P<chain_index>\d+)/editQuestion/(?P<question_index>\d+)/editOptions/$', views.editOptions, name='editOptions'),

)

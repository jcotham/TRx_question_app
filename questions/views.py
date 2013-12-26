from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from questions.models import QuestionProject, QuestionChain, Question, Option

# Create your views here.
def home(request):
  return render(request, 'questions/home.html')

#pages seen from Home
def index(request):
  return render(request, 'questions/index.html')
def existingProject(request):
  return render(request, 'questions/existing.html')

def addProject(request):
  if request.method == 'POST': # If the form has been submitted...
    form = NewProjectForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
     # Process the data in form.cleaned_data
       # ...
      #return HttpResponseRedirect('/thanks/') # Redirect after POST
      name = request.POST['name']
      qs = QuestionProject(project_name=name)
      qs.save()
      #request.session['project_name'] = request.POST['name']
      #request.session['index'] = qs.id
      return HttpResponseRedirect("/questions/editProject/%s/" % qs.id)#check if worked
  else:
    form = NewProjectForm() # An unbound form
  return render(request, 'questions/add.html', {
    'form': form,
  })


def addChain(request, project_index):
  if request.method == 'POST': # If the form has been submitted...
    form = NewChainForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      name = request.POST['name']
      qc = QuestionChain(chain_name=name)
      qc.save()

      # Project index?

      #request.session['project_name'] = request.POST['name']
      #request.session['index'] = qc.id
      return HttpResponseRedirect("/questions/editProject/%s/editChain/%s/" % (project_index, qc.id))#check if worked
  else:
    form = NewChainForm() # An unbound form
  return render(request, 'questions/addChain.html', {
    'form': form,
  })

def addQuestion(request, chain_index, project_index):
  if request.method == 'POST':
    form = NewQuestionForm(request.POST)
    if form.is_valid():
      ques_type = request.POST['question_type']
      ques_text = request.POST['question_text']
      disp_text  = request.POST['display_text']
      disp_group = request.POST['display_group']

      q = Question(question_text = ques_text, question_type = ques_type,
                   display_text = disp_text, display_group = disp_group)
      q.save()

      #redirect to options page unless fill in the blank
      if (ques_type == "fib"):
        return HttpResponseRedirect("/questions/editProject/%s/editChain/%s/" % (project_index, chain_index))
      return HttpResponseRedirect("/questions/editProject/%s/editChain/%s/editQuestion/%s/addOptions" % (project_index, chain_index, q.id))

  else:
    form = NewQuestionForm()
  return render(request, 'questions/addQuestion.html', {
    'form': form,
  })

def addOptions(request, question_index, chain_index, project_index):
  if request.method == 'POST':
    form = NewOptionForm(request.POST)
    if form.is_valid():
      #opts.save()
      return HttpResponseRedirect("/questions/editProject/%s/editChain/%s/" % (project_index, chain_index))
  else:
    form = NewOptionForm()
  return render(request, 'questions/addOptions.html', {
    'form': form,
  })



def editProject(request,project_index):
  dic = {"project_index":project_index, "form": NewChainForm()}
  return render(request, 'questions/editProject.html', dic)

def editChain(request,project_index,chain_index):
  return render(request, 'questions/editChain.html', { "project_index": project_index, "chain_index" : chain_index })

def editQuestion(request,chain_index,project_index):
  return render(request, 'questions/editQuestion.html', { "project_index": project_index, "chain_index" : chain_index, "form":NewQuestionForm() })

def editOptions(request,chain_index,project_index,question_index):
  return render(request, 'questions/editOptions.html', { "project_index": project_index, "chain_index": chain_index, "question_index": question_index })

def add(request):
  if request.method == 'POST': # If the form has been submitted...
    form = NewProjectForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      name = request.POST['name']
      qs = QuestionProject(project_name=name)
      qs.save()
      return HttpResponseRedirect("/questions/editProject/%s/" % qs.id)#check if worked
  else:
    form = NewProjectForm() # An unbound form
  return render(request, 'questions/add.html', {
    'form': form,
  })

def chain(request):
  context = {}
  context["projects"] = QuestionProject.objects.all()
  return render(request, 'questions/chain.html', context)

class NewProjectForm(forms.Form):
  name = forms.CharField(max_length=100)
class NewChainForm(forms.Form):
  name = forms.CharField(max_length=100)
class NewQuestionForm(forms.Form):
  question_text = forms.CharField(max_length=300, required=True)
  display_text = forms.CharField(max_length=100, required=True)
  display_group = forms.CharField(max_length=30, required=True)
  question_type = forms.ChoiceField(choices=[('fib','fill-in-the-blank'),
    ('yn','yes/no'),('cb','check box'),('cbb','check box with blank')])
class NewOptionForm(forms.Form):
  #add branching somehow
  text = forms.CharField(max_length=50)
  display_text = forms.CharField(max_length=10)
  highlight = forms.CharField(max_length=2)

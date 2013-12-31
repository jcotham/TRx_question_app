from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms.formsets import formset_factory
from questions.models import QuestionProject, QuestionChain, Question, Option, QuestionProjectToChain, ChainToQuestion

#################################### Home Pages ######################################

def projectHome(request):
  context = {}
  if request.method == 'POST':
    form = NewProjectForm(request.POST)
    if form.is_valid():
      name = request.POST['name']
      qp = QuestionProject(project_name=name)
      qp.save()

  context["projects"] = QuestionProject.objects.all()
  context["form"] = NewProjectForm()
  context["menu_location"] = "project"
  return render(request, 'questions/projectHome.html', context)

def chainHome(request):
  context = {}
  if request.method == 'POST':
    form = NewChainForm(request.POST)
    if form.is_valid():
      name = request.POST['name']
      qc = QuestionChain(chain_name=name)
      qc.save()

  context["chains"] = QuestionChain.objects.all()
  context["form"] = NewChainForm()
  context["menu_location"] = "chain"
  return render(request, 'questions/chainHome.html', context)


def questionHome(request):
  context = { "questions": Question.objects.all() }
  context["menu_location"] = "questions"
  return render(request, 'questions/questionHome.html', context)


#################################### Add Pages  ######################################

def addProject(request):
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


def addChain(request, project_index):
  if request.method == 'POST': # If the form has been submitted...
    form = NewChainForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      name = request.POST['name']
      qc = QuestionChain(chain_name=name)
      qc.save()

      return HttpResponseRedirect("/questions/editProject/%s/editChain/%s/" % (project_index, qc.id))#check if worked
  else:
    form = NewChainForm() # An unbound form
  return render(request, 'questions/addChain.html', {
    'form': form,
  })



def addQuestion(request):
  return editQuestion(request=request, question_index=-1)

# also editQuestion
def editQuestion(request, question_index):

  NewOptionsFormset = formset_factory(NewOptionForm, max_num=15, extra=0)
  if request.method == 'POST': # receiving question info
    if question_index == -1: # Saving new question
      print(request.POST)
      question_form = NewQuestionForm(request.POST)
      options_formset = NewOptionsFormset(request.POST, request.FILES)

      if question_form.is_valid() and options_formset.is_valid():
        ques_type = request.POST['question_type']
        ques_text = request.POST['question_text']
        disp_text  = request.POST['display_text']
        disp_group = request.POST['display_group']

        q = Question(question_text = ques_text, question_type = ques_type,
                     display_text = disp_text, display_group = disp_group)
        q.save()
        print("saving question...")

        for form in options_formset.forms:
          option = form.save(commit=False) #commit = false
          option.question = q
          option.save()
          print("saving option: " + str(option.display_text) + " belongs to: " + str(option.question.id))

        #redirect to options page unless fill in the blank
        return HttpResponseRedirect("/questions/questions")
    else: # Updating existing question
      print("sup")
      # TODO: this


  else: # render page
    NewOptionsFormset = formset_factory(NewOptionForm, max_num=15, extra=1)
    if question_index == -1:
      question_form = NewQuestionForm()
      options_formset = NewOptionsFormset()
    else: ##** The else statement needs to load the forms with data from database
      question = get_object_or_404(Question, id=question_index)
      options =  Option.objects.all().filter(question=question).values()
      question_form = NewQuestionForm(instance=question)
      print("options ===> ", options)
      options_formset = NewOptionsFormset(initial=options)
  return render(request, 'questions/addQuestion.html', {
    'question_form': question_form,
    'options_formset': options_formset,
  })



###################################  Save Pages     ##################################

# Not finished. Receiving a list of (hopefully) sorted
# question_chain ids that should be saved to the project_index
def saveProject(request, project_index):
  project_index = int(project_index)
  project_ids = request.POST.getlist('used_ids[]')
#  for p in project_ids: print(p)

  QuestionProjectToChain.objects.filter(question_set=project_index).delete()
  for i,p in enumerate(project_ids):
    p = int(p)
    print(project_index, p, i)
    try:
      qp_to_qc = QuestionProjectToChain(question_set_id=project_index, question_chain_id=p, stack_index=i)
    except Exception as e:
      print(e)
    qp_to_qc.save()

  return HttpResponse('')


def saveChain(request, chain_index):
  chain_index = int(chain_index)
  chain_ids = request.POST.getlist('used_ids[]')
  print(str(chain_ids) + "testing")
  ChainToQuestion.objects.filter(chain=chain_index).delete()
  for i,p in enumerate(chain_ids):
    p = int(p)
    #print(chain_index, p, i)
    try:
      qc_to_q = ChainToQuestion(chain_id=chain_index, question_id=p, chain_index=i)
    except Exception as e:
      print(e)
    qc_to_q.save()

  return HttpResponse('')

###################################  Edit Pages     ##################################

# TODO: Works, but hackish. Fix up later, when know how.
def editProject(request,project_index):
  project_index = int(project_index)
  dict = {}
  dict["project_index"] = project_index
  dict["project_name"] = QuestionProject.objects.get(id=project_index).project_name
  dict["form"] = NewChainForm()

  # Want used_chains to contains the question_chains that are used in the current project
  # and ununsed_chains to contain every other question_chain
  # used_qc_ids is a list of question_chain objects that relate to the matching QuestionProjectToChain entries
  qp_to_chain = QuestionProjectToChain.objects.all().filter(question_set=project_index)

  used_qc_ids = [e.question_chain_id for e in qp_to_chain]

  #for e in used_qc_ids: print e

  question_chains = QuestionChain.objects.all()

  # The idea is to sort the chains currently in use in the project by stack index. Untested as of yet
  dict["used_chains"] = sorted([e for e in question_chains if e.id in used_qc_ids],
      key=lambda k: [f for f in qp_to_chain if f.question_chain_id == k.id][0].stack_index)
  dict["unused_chains"] = sorted(list(set(question_chains)-set(dict["used_chains"])), key=lambda k: k.chain_name) # alphabetical

  return render(request, 'questions/editProject.html', dict)


def editChain(request,chain_index,project_index=0):
  chain_index = int(chain_index)
  dict = {}
  dict["chain_index"] = chain_index
  dict["chain_name"] = QuestionChain.objects.get(id=chain_index).chain_name

  chain_to_q = ChainToQuestion.objects.all().filter(chain=chain_index)
  used_question_ids = [e.question_id for e in chain_to_q]

  questions = Question.objects.all()

  dict["used_questions"] = sorted([e for e in questions if e.id in used_question_ids],
      key=lambda k: [f for f in chain_to_q if f.question_id == k.id][0].chain_index)
  dict["unused_questions"] = sorted(list(set(questions)-set(dict["used_questions"])), key=lambda k: k.display_group)

  return render(request, 'questions/editChain.html', dict)



def editOptions(request,chain_index,project_index,question_index):
  return render(request, 'questions/editOptions.html', { "project_index": project_index, "chain_index": chain_index, "question_index": question_index })


###################################  Delete Methods ##################################

def deleteProject(request, project_index):
  project = QuestionProject.objects.get(id = project_index)
  project.delete()
  return projectHome(request)


def deleteChain(request, chain_index):
  chain = QuestionChain.objects.get(id = chain_index)
  chain.delete()
  return chainHome(request)

def deleteQuestion(request, question_index):
  question = Question.objects.get(id = question_index)
  question.delete()
  return questionHome(request)

###################################  Forms          ##################################

class NewProjectForm(forms.Form):
  name = forms.CharField(max_length=100)
class NewChainForm(forms.Form):
  name = forms.CharField(max_length=100)

class NewQuestionForm(forms.ModelForm):
  class Meta:
    model= Question
    widgets = {
        'question_text': forms.Textarea(attrs={'cols':80, 'rows':2}),
        'translation_text': forms.Textarea(attrs={'cols':80, 'rows':2}),
        'display_text': forms.TextInput(attrs={'size':30}),
    }

class NewOptionForm(forms.ModelForm):
  class Meta:
    model = Option
    exclude = ['question']
    widgets = {
        'text': forms.TextInput(attrs={'size':40}),
        'highlight': forms.Select(),
        #'highlight': forms.TextInput(attrs={'size':3}),
    }



###################################  Miscellaneus   ##################################

def generateJSON(request, project_index):
  print("Generating JSON...")

from django.db import models

# Create your models here.
class QuestionProject(models.Model):
  project_name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.set_name

class QuestionChain(models.Model):
  chain_name = models.CharField(max_length=50)

  def __str__(self):
    return self.chain_name

class Question(models.Model):
  question_type = models.CharField(max_length=5)
  question_text = models.CharField(max_length=300)
  display_text = models.CharField(max_length=100)
  display_group = models.CharField(max_length=30)

  def __str__(self):
    return self.question_text

class Option(models.Model):
  question = models.ForeignKey(Question)
  branch = models.ForeignKey(QuestionChain)
  text = models.CharField(max_length=50)
  display_text = models.CharField(max_length=10)
  highlight = models.CharField(max_length=2)

  def __str__(self):
    return self.text

class ChainToQuestion(models.Model):
  question = models.ForeignKey(Question)
  chain = models.ForeignKey(QuestionChain)
  chain_index = models.IntegerField()
  
class QuestionProjectToChain(models.Model):
  question_set = models.ForeignKey(QuestionProject)
  question_chain = models.ForeignKey(QuestionChain)
  stack_index = models.IntegerField()

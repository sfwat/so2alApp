from django.db import models

# Create your models here.


class Submitter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choice')
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    submitter = models.ForeignKey(Submitter, on_delete=models.CASCADE, related_name='answer')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return f"{self.submitter} {self.question}: {self.choice}"


